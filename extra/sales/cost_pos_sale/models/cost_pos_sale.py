# -*- coding: utf-8 -*-
from incore import api, fields, models
from incore.addons import decimal_precision as dp


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    costo_venta = fields.Float(compute='_costo_venta', digits=dp.get_precision('Product Price'), store=True)
    purchase_price_cost = fields.Float(string='Costo', digits=dp.get_precision('Product Price'))


    def _compute_costo_venta(self, order_id, product_id):
        frm_cur = self.env.user.company_id.currency_id
        to_cur = order_id.pricelist_id.currency_id
        purchase_price_cost = product_id.standard_price
        price = frm_cur._convert(
            purchase_price_cost, to_cur, order_id.company_id or self.env.user.company_id,
            order_id.date_order or fields.Date.today(), round=False)
        return price


    @api.model
    def _get_purchase_price_cost(self, pricelist, product, product_uom, date):
        frm_cur = self.env.user.company_id.currency_id
        to_cur = pricelist.currency_id
        purchase_price_cost = product.standard_price
        price = frm_cur._convert(
            purchase_price_cost, to_cur,
            self.order_id.company_id or self.env.user.company_id,
            date or fields.Date.today(), round=False)
        return {'purchase_price_cost': price}


    @api.onchange('product_id')
    def product_id_change_cost(self):
        if not self.order_id.pricelist_id or not self.product_id:
            return
        self.purchase_price_cost = self._compute_costo_venta(self.order_id, self.product_id)


    @api.model
    def create(self, vals):
        if 'purchase_price_cost' not in vals:
            order_id = self.env['pos.order'].browse(vals['order_id'])
            product_id = self.env['product.product'].browse(vals['product_id'])

            vals['purchase_price_cost'] = self._compute_costo_venta(order_id, product_id)

        return super(PosOrderLine, self).create(vals)


    @api.depends('product_id', 'purchase_price_cost', 'qty', 'price_unit', 'price_subtotal')
    def _costo_venta(self):
        for line in self:
            currency = line.order_id.pricelist_id.currency_id
            price = line.purchase_price_cost
            line.costo_venta = currency.round(price * line.qty)


class PosOrder(models.Model):
    _inherit = "pos.order"


    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True, required=True)
    costo_venta = fields.Monetary(compute='_costo_venta',
        currency_field='currency_id', 
        digits=dp.get_precision('Product Price'), store=True)


    @api.depends('lines.costo_venta')
    def _costo_venta(self):
        for order in self:
            order.costo_venta = sum(order.lines.filtered(lambda r: r.qty != 0).mapped('costo_venta'))


    @api.model
    def _execute_update_cost(self):
        orders = self.env['pos.order'].search([])

        for order in orders:
            for line in order.order_line:
                line.product_id_change_cost()
                line._costo_venta()
            order._costo_venta()

#