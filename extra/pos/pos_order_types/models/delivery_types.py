# -*- coding: utf-8 -*-

from incore import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    delivery_type = fields.Many2one('delivery.type', string='Order Type', readonly=True)

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['delivery_type'] = ui_order.get('delivery_method_id', False)
        return order_fields


class DeliveryMethods(models.Model):
    _inherit = 'pos.config'

    enable_delivery = fields.Boolean(string='Enable Order Types')
    delivery_methods = fields.Many2many('delivery.type', string='Order Types')


class DeliveryTypes(models.Model):
    _name = 'delivery.type'

    name = fields.Char('Order Type')
