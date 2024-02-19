# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models

class Company(models.Model):
    _inherit = "res.company"

    snailmail_color = fields.Boolean(string='Color', default=False)
    snailmail_duplex = fields.Boolean(string='Both sides', default=False)
