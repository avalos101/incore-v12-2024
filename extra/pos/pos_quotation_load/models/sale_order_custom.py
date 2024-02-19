# -*- coding: utf-8 -*-
from incore import models,fields

class SaleOrderInherit(models.Model):
    _inherit='sale.order'
    
    pos_order_ref = fields.Char('Pos Order Reference',copy=False)
    pos_sync = fields.Boolean('Pos Order Sync',copy=False)    