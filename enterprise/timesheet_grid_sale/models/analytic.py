# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models
from incore.osv import expression


class AnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    def _get_adjust_grid_domain(self, column_value):
        """ Don't adjust already invoiced timesheet """
        domain = super(AnalyticLine, self)._get_adjust_grid_domain(column_value)
        return expression.AND([domain, [('timesheet_invoice_id', '=', False)]])
