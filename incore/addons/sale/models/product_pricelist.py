# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    discount_policy = fields.Selection([
        ('with_discount', 'Discount included in the price'),
        ('without_discount', 'Show public price & discount to the customer')],
        default='with_discount')
