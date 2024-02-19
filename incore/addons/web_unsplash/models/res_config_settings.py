# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
from incore import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    unsplash_access_key = fields.Char("Access Key", config_parameter='unsplash.access_key')
