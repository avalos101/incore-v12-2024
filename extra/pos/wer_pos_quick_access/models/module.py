# -*- coding: utf-8 -*-

from incore import models, fields, api, tools, _

class PosConfig(models.Model):
    _inherit = 'pos.config'

    change_product_view = fields.Boolean(string='Product View', help="=Help to View Products in List/Grid View")
    quick_partner = fields.Boolean(string='Create Partner', help="Allow User to Create Customer from Product Screen")
    quick_product = fields.Boolean(string='Create Product', help="Allow User to Create Product from POS Screen")
    clear_cart = fields.Boolean(string='Clear Cart', help="Allow User to Clear Products from Cart")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create_partner(self,fields):
    	partner_id = self.create(fields)
    	return partner_id.read()


class Product_product(models.Model):
    _inherit = 'product.product'

    @api.model
    def create_product(self,fields):
    	product_id = self.create(fields)
    	return product_id.read()