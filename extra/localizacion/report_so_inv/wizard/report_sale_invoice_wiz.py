# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from incore import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)

class ReportWiz(models.TransientModel):
	_name = "report.payment.so.inv.wiz"
	_description = "Reporte de pagos de Pedidos POS y Facturas"

	# user_id = fields.Many2one('res.users', string="Vendedor", required=True)
	user_ids = fields.Many2many('res.users','users_report_so_inv_rel','user_id','report_id', string="Cajero", required=True)
	start_date = fields.Date(string='Fecha Inicio', required=True)
	end_date = fields.Date(string='Fecha Fin', required=True)

	@api.multi
	def print_report(self):
		data = {'date_start': self.start_date, 'date_stop': self.end_date, 'user_ids': self.user_ids.ids}
		return self.env.ref('report_so_inv.inv_sale_report').report_action(self, data=data)