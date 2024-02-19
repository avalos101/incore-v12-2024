# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.

from incore import models, fields
from incore.tools.translate import _


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
            ('weight', 'Weighted Product'),
            ('price', 'Priced Product'),
            ('discount', 'Discounted Product'),
            ('client', 'Client'),
            ('cashier', 'Cashier')
        ])
