# -*- coding: utf-8 -*-
from incore import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    auto_merge_invoice_line = fields.Boolean(string="Auto Merge Invoice Lines")
    auto_merge_bill_line = fields.Boolean(string="Auto Merge Bill Lines")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_merge_invoice_line = fields.Boolean(string="Auto Merge Invoice Lines", related='company_id.auto_merge_invoice_line', readonly=False)
    auto_merge_bill_line = fields.Boolean(string="Auto Merge Bill Lines", related='company_id.auto_merge_bill_line', readonly=False)
