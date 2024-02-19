# -*- coding: utf-8 -*-
from incore import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    costo_venta = fields.Float('Costo Venta')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['costo_venta'] = ", SUM(l.costo_venta / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS costo_venta"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)