# -*- coding: utf-8 -*-
from incore import models,fields,api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    sh_enable_quotation_load = fields.Boolean("Enable Quotation Load")

class PosOrderInherit(models.Model):
    _inherit='pos.order'
    
    sale_order_id = fields.Many2one('sale.order','Sale Order Reference')
    sale_order_name = fields.Char('Sale Order')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrderInherit,self)._order_fields(ui_order)
        if res:            
            if ui_order.get('sale_order_id',False):
                so = self.env['sale.order'].search([('id','=',ui_order['sale_order_id']),('state','in',['draft','sent'])],limit=1)
                if so:
                    res.update({'sale_order_id':so.id})                
                    so.action_cancel()
                    so.pos_sync = True
                    so.pos_order_ref = ui_order['name']
        return res            