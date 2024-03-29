# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    team_id = fields.Many2one('crm.team', string='Sales Team')

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", sub.team_id as team_id"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + ", ai.team_id as team_id"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", ai.team_id"
