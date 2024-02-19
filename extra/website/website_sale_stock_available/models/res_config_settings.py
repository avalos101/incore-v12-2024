# -*- coding: utf-8 -*-
# Part of Incore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inventory_availability = fields.Selection(selection_add=[
        ('not_show', 'Not show the product variants if it is not available.')])
