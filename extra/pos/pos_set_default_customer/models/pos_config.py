# -*- coding: utf-8 -*-
from incore import fields, models


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    default_partner_id = fields.Many2one('res.partner', string="Select Customer", domain="[('customer','=',True)]")
