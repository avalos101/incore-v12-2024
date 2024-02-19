# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models, fields, _


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
            ('weight', 'Weighted Product'),
            ('location', 'Location'),
            ('lot', 'Lot'),
            ('package', 'Package')
        ])
