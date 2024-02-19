# -*- coding: utf-8 -*-

from incore import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_l10n_mx_edi = fields.Boolean('Mexican Electronic Invoicing')
