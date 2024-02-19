# -*- coding: utf-8 -*-
from incore import tools
from incore import api, fields, models


class PosSaleReport(models.Model):
    _name = "pos.sale.report"
    _auto = False
    _description = "Report POS Sale"

    id = fields.Integer('ID')
    product_id = fields.Many2one('product.product', 'Product', readonly = True)
    product_tmpl_id = fields.Many2one('product.template', 'Product template', readonly = True)
    product_uom = fields.Many2one('uom.uom', 'Uom', readonly=True)
    qty = fields.Float('Quantity', readonly=True)
    price_total = fields.Float('Price total', readonly=True)
    price_subtotal = fields.Float('Price subtotal', readonly=True)
    price_subtotal_incl = fields.Float('Price subtotal Incl', readonly=True)
    rec = fields.Integer('Records', readonly=True)
    name = fields.Char('Pos Order', readonly=True)
    date = fields.Datetime('Order Date', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancelled'),
        ('paid', 'Paid'),
        ('done', 'Done'),
        ('invoiced', 'Invoiced'),
        ], string='Status', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly = True)
    user_id = fields.Many2one('res.users', 'User', readonly = True)
    company_id = fields.Many2one('res.company', 'Company', readonly = True)
    categ_id = fields.Many2one('res.company', 'Category', readonly = True)
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', readonly = True)
    country_id = fields.Many2one('res.country', 'Country', readonly = True)
    commercial_partner_id = fields.Many2one('res.partner', 'Commercial partner', readonly = True)
    weight = fields.Float('Weight', readonly=True)
    volume = fields.Float('Volume', readonly=True)
    discount = fields.Float('Discount', readonly=True)
    discount_amount = fields.Float('Discount amount', readonly=True)
    order_id = fields.Many2one('pos.order', 'Order ID', readonly = True)
    costo_venta = fields.Float('Costo venta', readonly=True)


    def _select(self):
        select_str = """
			SELECT min(l.id) AS id,
                l.product_id AS product_id,
                t.uom_id AS product_uom,
                sum(l.qty) AS qty,
                sum((l.qty * l.price_unit) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_total,
                sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_subtotal,
                sum(l.price_subtotal_incl / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_subtotal_incl,
                count(*) AS rec,
                s.name AS name,
                s.date_order AS date,
                s.state AS state,
                s.partner_id AS partner_id,
                s.user_id AS user_id,
                c.id AS company_id,
                cat.id AS categ_id,
                s.pricelist_id AS pricelist_id,
                p.product_tmpl_id AS product_tmpl_id,
                partner.country_id AS country_id,
                partner.commercial_partner_id AS commercial_partner_id,
                sum(p.weight * l.qty) AS weight,
                sum(p.volume * l.qty) AS volume,
                l.discount AS discount,
                sum((l.price_unit * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) AS discount_amount,
                s.id AS order_id,
                SUM(l.costo_venta / CASE COALESCE(s.currency_rate, 0) 
                    WHEN 0 
                    THEN 1.0 
                    ELSE s.currency_rate 
                    END) 
                AS costo_venta
		"""

        return select_str


    def _from(self):


        from_str = """
            FROM pos_order_line l
                join pos_order s on (l.order_id=s.id)
                left join res_partner partner on (s.partner_id = partner.id)
                left join res_company c on (s.company_id = c.id)
                left join product_product p on (l.product_id=p.id)
                left join product_template t on (p.product_tmpl_id=t.id)
                left join product_category cat on (cat.id=t.categ_id)
                left join uom_uom u on (u.id=t.uom_id)
                left join product_pricelist pp on (s.pricelist_id = pp.id)
            WHERE l.product_id IS NOT NULL 
		"""
        return from_str


    def _group_by(self):
        group_by_str = """
            GROUP BY l.product_id,
                l.order_id,
                t.uom_id,
                t.categ_id,
                cat.id,
                s.name,
                s.partner_id,
                s.user_id,
                s.state,
                s.company_id,
                s.pricelist_id,
                p.product_tmpl_id,
                partner.country_id,
                partner.commercial_partner_id,
                l.discount,
                s.id,
                c.id
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        sql = """CREATE or REPLACE VIEW %s as (%s %s %s)""" % (self._table, self._select(), self._from(), self._group_by())
        self.env.cr.execute(sql)

#