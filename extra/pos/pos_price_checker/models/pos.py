# -*- coding: utf-8 -*-


from incore import fields, models,tools,api


class pos_config(models.Model):
    _inherit = 'pos.config' 
    
    allow_price_checker = fields.Boolean("Allow Price Checker")

    