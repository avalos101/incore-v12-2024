# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    extract_show_ocr_option_selection = fields.Selection(related='company_id.extract_show_ocr_option_selection', string='Automatic Bills Processing', readonly=False)