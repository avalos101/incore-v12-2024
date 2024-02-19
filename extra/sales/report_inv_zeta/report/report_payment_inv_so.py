# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
import logging
from datetime import datetime, timedelta
from functools import partial

import psycopg2
import pytz

from incore import api, fields, models, tools, _
from incore.tools import float_is_zero
from incore.exceptions import UserError
from incore.http import request
from incore.addons import decimal_precision as dp

from collections import Counter

_logger = logging.getLogger(__name__)


class ReportDetails(models.AbstractModel):

	_name = 'report.report_inv_zeta.report_inv_detail'
	_description = 'Total de Pedidos y Facturas'


	@api.model
	def get_invoice_details(self, date_start=False, date_stop=False, users=False):

		user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
		date_start = fields.Date.from_string(date_start)
		date_stop = fields.Date.from_string(date_stop)
		# avoid a date_stop smaller than date_start
		date_stop = max(date_stop, date_start)

		date_start = fields.Date.to_string(date_start)
		date_stop = fields.Date.to_string(date_stop)

		invoices = self.env['account.invoice'].sudo().search([
			('date_invoice', '>=', date_start),
			('date_invoice', '<=', date_stop),
			('user_id', 'in', users.ids),
			('state', 'not in', ['draft','cancel']),
			('type', '=', 'out_invoice')], order="number asc")

		total_i, tax_inv, total_inv, disc_inv = 0.0,0.0,0.0,0.0
		p_iniciales = 0.0
		taxes_inv = {}
		totales_tax = {}
		totales_pay = {}

		for inv in invoices:
			tax_inv += inv.amount_tax
			total_inv += inv.amount_total
			# Removed percentage
			# Author: Leon Avalos on June 3 
			#disc_inv += sum(l.quantity * l.price_unit * ((l.discount or 0.0) / 100.0) for l in inv.invoice_line_ids)
			disc_inv += sum(l.quantity * l.price_unit * ((l.discount or 0.0) / 100.0) for l in inv.invoice_line_ids)
			for line in inv.invoice_line_ids:
				price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
				taxes = line.invoice_line_tax_ids.compute_all(price_unit, inv.currency_id, line.quantity, line.product_id, inv.partner_id)['taxes']
				for tax in taxes:
					taxes_inv.setdefault(tax['id'], {'name': tax['name'], 'tax_amount':0.0, 'base_amount':0.0})
					taxes_inv[tax['id']]['tax_amount'] += tax['amount']
					taxes_inv[tax['id']]['base_amount'] += tax['base']
					totales_tax.setdefault(tax['id'], {'name': tax['name'], 'tax_amount':0.0, 'base_amount':0.0})
					totales_tax[tax['id']]['tax_amount'] += tax['amount']
					totales_tax[tax['id']]['base_amount'] += tax['base']
					total_i += tax['base'] + tax['amount']
				if not taxes:
					taxes_inv.setdefault(0, {'name': u'Admon', 'tax_amount':0.0, 'base_amount':0.0})
					taxes_inv[0]['base_amount'] += line.price_subtotal
					totales_tax.setdefault(0, {'name': u'Admon', 'tax_amount':0.0, 'base_amount':0.0})
					totales_tax[0]['base_amount'] += line.price_subtotal
					total_i += line.price_subtotal


		payments = self.env['account.payment'].sudo().search([
			('payment_date', '>=', date_start),
			('payment_date', '<=', date_stop),
			('state', '=', 'posted'),
			('create_uid', 'in', users.ids),
			('partner_type', '=', 'customer'),
			('payment_type', '=', 'inbound')], order="create_uid asc")

		journals_pay = {}
		for pay in payments:
			if 'hfoc_inicial' in pay._fields:
				if pay.hfoc_inicial:
					p_iniciales += pay.amount

			journals_pay.setdefault(pay.journal_id.id, [pay.journal_id.name, 0.0])
			journals_pay[pay.journal_id.id][1] += pay.amount
			totales_pay.setdefault(pay.journal_id.id, [pay.journal_id.name, 0.0])
			totales_pay[pay.journal_id.id][1] += pay.amount
		user_currency = self.env.user.company_id.currency_id
		consecutivo = {}
		if invoices:
			consecutivo.setdefault(0,["Consecutivo Inicial",invoices[0].number])
			consecutivo.setdefault(1,["Consecutivo Final",invoices[len(invoices)-1].number])


		return {
			'company' : self.env.user.company_id,
			'currency_precision': user_currency.decimal_places,
			'currency_id': user_currency,
			'count_inv': len(invoices),
			'tax_inv' : tax_inv,
			'total_inv' : total_inv,
			'p_iniciales': p_iniciales,
			'total_i' : total_i + disc_inv,
			'disc_inv' : disc_inv,
			'journals' : journals_pay,
			'taxes_inv' : list(taxes_inv.values()),
			'journals_pay' : list(journals_pay.values()),
			'totales_tax' : list(totales_tax.values()),
			'totales_pay' : list(totales_pay.values()),
			'consecutivos' : list(consecutivo.values()),
			'user_ventas' : users,
		}



	@api.multi
	def _get_report_values(self, docids, data=None):
		data = dict(data or {})
		users = self.env['res.users'].browse(data['user_ids'])
		data.update(self.get_invoice_details(data['date_start'], data['date_stop'], users))
		return data