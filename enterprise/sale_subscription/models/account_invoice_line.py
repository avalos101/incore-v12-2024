# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
from incore import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    subscription_id = fields.Many2one('sale.subscription')
