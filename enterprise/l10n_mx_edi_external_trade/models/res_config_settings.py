# -*- coding: utf-8 -*-

from incore import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_mx_edi_num_exporter = fields.Char(
        related='company_id.l10n_mx_edi_num_exporter', readonly=False,
        string='Number of Reliable Exporter')
