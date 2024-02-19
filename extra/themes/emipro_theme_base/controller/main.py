import incore
from incore import http,fields,tools, _
from incore.http import request
from incore.tools.safe_eval import safe_eval
from incore.addons.http_routing.models.ir_http import slug
from incore.addons.website.controllers.main import QueryURL
from incore.exceptions import ValidationError
from incore.addons.website.controllers.main import Website

from incore.addons.website_sale.controllers.main import WebsiteSale
from incore.addons.website_sale.controllers.main import TableCompute
from incore.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist




PPG = 20
PPR = 4


class claricoQuickView(http.Controller):
    
    @http.route(['/productdata'], type='json', auth="public", website=True)    
    def fetchProduct(self,product_id=None, **kwargs):
        if product_id :
            product_record = request.env['product.template'].search([['id','=',product_id]])
            
            pricelist = request.website.get_current_pricelist()
            
            from_currency = request.env.user.company_id.currency_id
            to_currency = pricelist.currency_id
            compute_currency = lambda price: from_currency.compute(price, to_currency)
            
            values={
                'product':product_record,
                #'get_attribute_value_ids': self.get_attribute_value_ids,
                'compute_currency': compute_currency,
                'get_attribute_exclusions': self._get_attribute_exclusions
            }

            product = request.env['product.template'].search([['id','=',product_id]])
            response = http.Response(template="emipro_theme_base.theme_quickview_template",qcontext=values)            
        return response.render()
    
    def _get_attribute_exclusions(self, product, reference_product=None):
        """ list of attribute exclusions of a product

        Args:
            - product (product.template): The base product template
            - reference_product (product.product): The reference product from which 'product' is an optional or accessory product

        :return: dict of exclusions
           exclusions.exclusions: exclusions within this product
           exclusions.parent_exclusions: exclusions coming from the reference_product
        """

        product_attribute_values = request.env['product.template.attribute.value'].search([
            ('product_tmpl_id', '=', product.id),
            ('product_attribute_value_id', 'in', product.attribute_line_ids.mapped('value_ids').ids),
        ])

        # array of all the excluded value_ids of all the filter lines for this product
        mapped_exclusions = {
            product_attribute_value.id: [
                value_id
                for filter_line in product_attribute_value.exclude_for.filtered(
                    lambda filter_line: filter_line.product_tmpl_id == product
                ) for value_id in filter_line.value_ids.ids
            ]
            for product_attribute_value in product_attribute_values
        }

        parent_exclusions = []
        if reference_product:
            parent_attribute_value_ids = reference_product.product_template_attribute_value_ids
            if parent_attribute_value_ids and reference_product._context.get('no_variant_attribute_values'):
                # Add "no_variant" attribute values' exclusions
                # They are kept in the context since they are not linked to this product variant
                parent_attribute_value_ids |= reference_product._context.get('no_variant_attribute_values')

            parent_exclusions = [
                value_id
                for filter_line in parent_attribute_value_ids.mapped('exclude_for').filtered(
                    lambda filter_line: filter_line.product_tmpl_id == product
                ) for value_id in filter_line.value_ids.ids]

        # Query all archived products for this template
        archived_combinations = request.env['product.product'].search(
            [('product_tmpl_id', '=', product.id), ('active', '=', False)])

        if archived_combinations:
            # Old archived variants could have a different set of attributes and are not relevant here
            # -> filter them out
            attribute_ids = product_attribute_values.mapped('attribute_id')
            archived_combinations = archived_combinations.filtered(
                lambda product: all(
                    attribute_id in product.mapped('product_template_attribute_value_ids.attribute_id')
                    for attribute_id in attribute_ids
                )
            )

        return {
            'exclusions': mapped_exclusions,
            'parent_exclusions': parent_exclusions,
            'archived_combinations': [archived_combination.product_template_attribute_value_ids.ids
                for archived_combination in archived_combinations]
        }
    
    def get_attribute_value_ids(self, product):
        product = product.with_context(quantity=1)

        visible_attrs_ids = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped('attribute_id').ids
        to_currency = request.website.get_current_pricelist().currency_id
        attribute_value_ids = []
        for variant in product.product_variant_ids:
            if to_currency != product.currency_id:
                price = variant.currency_id.compute(variant.website_public_price, to_currency)
            else:
                price = variant.website_public_price
            visible_attribute_ids = [v.id for v in variant.attribute_value_ids if v.attribute_id.id in visible_attrs_ids]
            attribute_value_ids.append([variant.id, visible_attribute_ids, variant.website_price, price])
        return attribute_value_ids
    
class Slider(http.Controller):
    
    #Return The Slider Preview template 
    @http.route(['/slider-preview'], type='http', auth="public",website=True)
    def slider_preview(self,rec_id,**kwargs):
        return http.Response(template="emipro_theme_base.clarico_slider_preview", qcontext={'rec_id' : rec_id}).render()
    
    #Return the data for slider for product slider and category Slider
    # If filter ID is not specified then return first filter slider object else it return specified slider filter
    @http.route(['/slider/render'], type='json', auth="public",website=True)
    def slider_data(self, **kwargs):
        slider_id = kwargs.get('slider_id', False)
        filter_id = kwargs.get('filter_id', False)
        slider_obj = request.env['slider'].sudo().search([('id', '=', int(slider_id))])
        vals ={}
        if slider_obj:
            if slider_obj.slider_type == 'product':
                filter = slider_obj.slider_filter_ids[0] if not filter_id  else request.env['slider.filter'].sudo().search([('id', '=', int(filter_id))])
                if filter.filter_id.domain:
                    compute_currency, pricelist_context, pricelist =  WebsiteSale()._get_compute_currency_and_context()
                    domain = safe_eval(filter.filter_id.domain)
                    domain+=['|',('website_id', '=',None),('website_id', '=', request.website.id),('website_published','=',True)]
                    product = request.env['product.template'].sudo().search(domain,limit=slider_obj.slider_limit)
                    vals ={
                            'slider_obj':slider_obj,
                            'filter_data':product,
                            'compute_currency':compute_currency,
                            'active_filter_data':filter_id if filter_id else slider_obj.slider_filter_ids[0].id,
                            'is_default':False if filter_id else True
                        }
                tmplt_external_id=slider_obj.slider_style_id.get_external_id().get(slider_obj.slider_style_id.id)+"_template"
                tmplt=request.env['ir.ui.view'].sudo().search([('key','=',tmplt_external_id)])
                if tmplt:
                    response = http.Response(template=tmplt_external_id, qcontext=vals)
                    return response.render()
                else:
                    return False
            else:
                domain=[('website_id','in',(False,request.website.get_current_website().id)),('parent_id','=',False)]
                category = request.env['product.public.category'].sudo().search(domain,limit=slider_obj.slider_limit)
                return request.env.ref("emipro_theme_base.theme_category_carousel").render({'object':category})
        
class menuHtmlLayout(http.Controller):
    
    @http.route('/menu_html_builder', type='http', auth="user", website=True)
    def website_menu(self, model=False, id=False, **kw):
        if id and model:
            id = int(id)
            record = request.env[model].browse(id)
            values = {
                'record': record,
                'model': model,
                'id': id,
            }
            return request.render("emipro_theme_base.website_menu_edit",values)      
    
class themeBase(WebsiteSaleWishlist):
    
    @http.route(['/shop/wishlist'], type='http', auth="public", website=True)
    def get_wishlist(self, count=False, **kw):
        wishlist = request.env['product.wishlist'].with_context(display_default_code=False).current()
        wishlist_list = []
        for wish in wishlist:
            if wish.product_id.id in wishlist_list:
                wish.unlink()
                continue
            wishlist_list.append(wish.product_id.id)
        return super(themeBase, self).get_wishlist(count=count,**kw)

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        if not post.get('filter_id',False):
            return super(themeBase, self).shop(page=page, category=category, search=search, ppg=ppg,**post)

        # If the filter found replace domain with the filter domain and render the shop with default functionality
        slider_filter = request.env['slider.filter'].sudo().search([('id', '=', int(post.get('filter_id')))])
        if  not slider_filter:
            return request.redirect("/shop")

        domain = safe_eval(slider_filter.filter_id.domain)

        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        # domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))

        compute_currency, pricelist_context, pricelist = self._get_compute_currency_and_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template']

        Category = request.env['product.public.category']
        search_categories = False
        if search:
            categories = Product.search(domain).mapped('public_categ_ids')
            search_categories = Category.search([('id', 'parent_of', categories.ids)] + request.website.website_domain())
            categs = search_categories.filtered(lambda c: not c.parent_id)
        else:
            categs = Category.search([('parent_id', '=', False)] + request.website.website_domain())

        parent_category_ids = []
        if category:
            url = "/shop/category/%s" % slug(category)
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([('attribute_line_ids.product_tmpl_id', 'in', selected_products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
            'search_categories_ids': search_categories and search_categories.ids,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)
    
class BrandFilter(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        domain = super(BrandFilter, self)._get_search_domain(search=search,category=category,attrib_values=attrib_values)
        if attrib_values:
            ids = []
            for value in attrib_values:
                if value[0] == 0:
                    ids.append(value[1])
                    domain += [('product_brand_ept_id.id', 'in', ids)]
        return domain

class wishlist(WebsiteSale):
    @http.route(['/shop/wishlist/remove/<model("product.wishlist"):wish>'], type='json', auth="public", website=True)
    def rm_from_wishlist(self, wish, **kw):
        super(themeBase, self).rm_from_wishlist(wish=wish, **kw)
        if request.website.is_public_user():
            wish_ids = request.session.get('wishlist_ids') or []
            return len(wish_ids)
        remain_wish = request.env['product.wishlist'].sudo().search_count([('partner_id', '=', wish.partner_id.id), ('active', '=', True)])
        if remain_wish:
            return remain_wish