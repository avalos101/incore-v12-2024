# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from incore import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)

class ReporInvoicetWiz(models.TransientModel):
	_name = "report.invoice.zeta"
	_description = "Informe Zeta de Facturas"

	user_ids = fields.Many2many('res.users','users_report_inv_rel','user_id','report_id', string="Cajero", required=True)
	start_date = fields.Date(string='Fecha Inicio', required=True)
	end_date = fields.Date(string='Fecha Fin', required=True)

	@api.multi
	def print_report(self):
		data = {'date_start': self.start_date, 'date_stop': self.end_date, 'user_ids': self.user_ids.ids}
		return self.env.ref('report_inv_zeta.report_invoice_zeta').report_action(self, data=data)