from incore import api, fields, models
from incore.tools.translate import _
from datetime import date, datetime, timedelta
from incore.http import request 
 
class website(models.Model):
    _inherit = "website"
    
    is_brand_value_consider = fields.Boolean(string="Brand Value Consider")
   
    # to render main parent product.public.category website specific
    def category_check(self):
        return self.env['product.public.category'].sudo().search([('website_published','=',True),('parent_id', '=', False),('website_id', 'in', (False,self.id))])
    
    
    # to render full path for breadcrumbs based on argument
    # args : product.public.category
    # return : list of category path and website url
    def get_product_categs_path(self, id):
        categ_set = []
        if id:
            while id:
                categ = self.env['product.public.category'].sudo().search([('id', '=', id)])
                categ_set.append(categ.id)
                if categ and categ.parent_id:
                    id = categ.parent_id.id
                else:
                    break
            
        # For Reverse order
        categ_set = categ_set[::-1]
        
        values = {
            'categ_set': categ_set,
            'web_url': self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        }
        return values
    
    #Return The Current Pricelist Item For diplay a Offer In Slider 
    def get_pricelist_item_id(self,product):
        item_ids= self.get_current_pricelist().item_ids
        for item in item_ids:
            if item.date_end and item.date_end >= datetime.today().date():
                if item.applied_on == '0_product_variant':
                    if product.product_variant_id[0].id == item.product_id.id:
                        return item
                elif item.applied_on == '1_product':
                    if product.id == item.product_tmpl_id.id:
                        return item
                elif item.applied_on == '2_product_category':
                    if product.categ_id.id == item.categ_id.id :
                        return item
                elif item.applied_on == '3_global': 
                    return item
        return False
    
    def get_recently_viewed_items(self, product_id=False):
        recently_viewed_product_ids = request.session.get('recently_viewed_product_ids', False)
        if not recently_viewed_product_ids and not product_id:
            return False

        # set product id into session if it not into session if session is not than create a session
        if product_id:
            if recently_viewed_product_ids:
                if product_id not in request.session['recently_viewed_product_ids']:
                    if len(recently_viewed_product_ids)>=10:
                        recently_viewed_product_ids.pop()
                    tmp = recently_viewed_product_ids
                    tmp.insert(0, product_id)
                    request.session['recently_viewed_product_ids'] = tmp
                else:
                    recently_viewed_product_ids.remove(product_id)
                    tmp = recently_viewed_product_ids
                    tmp.insert(0, product_id)
                    request.session['recently_viewed_product_ids'] = tmp

            else:
                request.session['recently_viewed_product_ids'] = [product_id]

        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency._convert(price, to_currency, request.env.user.company_id,fields.Date.today())
        values = {            
            'recent_products': request.session.get('recently_viewed_product_ids', False),     
            'compute_currency': compute_currency        
            } 
        return values
    
    #method for price filter min max value
    def get_min_max_prices(self):
        range_list = []
        cust_min_val = request.httprequest.values.get('min_val',False)
        cust_max_val = request.httprequest.values.get('max_val',False)

        q = 'select min(list_price),max(list_price) from product_template where sale_ok=True and active=True'
        # q = 'select min(list_price),max(list_price) from product_template where sale_ok=True and active=True and website_id like (%d,FALSE)' % self.id
        request.cr.execute(q)
        min_max_vals = request.cr.fetchall()

        min_val = min_max_vals[0][0] or 0
        if int(min_val) == 0:
            min_val = 0
        max_val = min_max_vals[0][1] or 1

        if not cust_min_val and not cust_max_val:
            range_list.append(min_val)
            range_list.append(max_val)
            range_list.append(min_val)
            range_list.append(max_val)
        else:
            range_list.append(cust_min_val)
            range_list.append(cust_max_val)
            range_list.append(min_val)
            range_list.append(max_val)
        print(range_list)
        return range_list
    
    #return brand list
    def get_brand(self):
        brand_list = self.env['product.brand.ept'].sudo().search([('website_published','=',True),('website_id', 'in',(False,self.id))])
        return brand_list
