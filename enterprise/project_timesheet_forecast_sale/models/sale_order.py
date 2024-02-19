# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_project(self):
        return super(SaleOrderLine, self.with_context(default_allow_forecast=True))._timesheet_create_project()
