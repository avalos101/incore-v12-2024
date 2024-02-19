# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.

from incore import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ['utm.mixin', 'sale.order']
