# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_website_popup_on_exit = fields.Boolean(string="Website Popup", implied_group="website_mass_mailing.group_website_popup_on_exit")
