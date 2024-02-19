# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.
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

	_name = 'report.report_so_inv.report_inv_so_detail'
	_description = 'Total de Pedidos y Facturas'


	@api.model
	def get_sale_details(self, date_start=False, date_stop=False, users=False):

		user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
		date_start = fields.Date.from_string(date_start)
		date_stop = fields.Date.from_string(date_stop)
		# avoid a date_stop smaller than date_start
		date_stop = max(date_stop, date_start)

		date_start = fields.Date.to_string(date_start)
		date_stop = fields.Date.to_string(date_stop)
		total_p, tax_pos, total_pos, disc_pos = 0.0,0.0,0.0,0.0
		journals_pos = {}
		taxes_pos = {}
		totales_tax = {}
		totales_pay = {}

		orders = self.env['pos.order'].search([
			('date_order', '>=', date_start +' 00:00:00'),
			('date_order', '<=', date_stop + ' 23:59:59'),
			('state', 'in', ['paid','done']),
			('user_id', 'in', users.ids)], order="user_id asc")
		for order in orders:
			tax_pos += order.amount_tax
			total_pos += order.amount_total
			disc_pos += sum(l.qty * l.price_unit * ((l.discount or 0.0) / 100.0) for l in order.lines)
			currency = order.session_id.currency_id
			for line in order.lines:
				if line.tax_ids_after_fiscal_position:
					line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1-(line.discount or 0.0)/100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
					for tax in line_taxes['taxes']:
						taxes_pos.setdefault(tax['id'], {'name': tax['name'], 'tax_amount':0.0, 'base_amount':0.0})
						taxes_pos[tax['id']]['tax_amount'] += tax['amount']
						taxes_pos[tax['id']]['base_amount'] += tax['base']

						totales_tax.setdefault(tax['id'], {'name': tax['name'], 'tax_amount':0.0, 'base_amount':0.0})
						totales_tax[tax['id']]['tax_amount'] += tax['amount']
						totales_tax[tax['id']]['base_amount'] += tax['base']
						total_p += tax['base'] + tax['amount']
				else:
					taxes_pos.setdefault(0, {'name': u'Admon', 'tax_amount':0.0, 'base_amount':0.0})
					taxes_pos[0]['base_amount'] += line.price_subtotal_incl

					totales_tax.setdefault(0, {'name': u'Admon', 'tax_amount':0.0, 'base_amount':0.0})
					totales_tax[0]['base_amount'] += line.price_subtotal_incl
					total_p += line.price_subtotal_incl


		st_line_ids = self.env["account.bank.statement.line"].search([('pos_statement_id', 'in', orders.ids)]).ids
		if st_line_ids:
			self.env.cr.execute("""
			    SELECT aj.id, aj.name, sum(amount) total
			    FROM account_bank_statement_line AS absl,
			         account_bank_statement AS abs,
			         account_journal AS aj 
			    WHERE absl.statement_id = abs.id
			        AND abs.journal_id = aj.id 
			        AND absl.id IN %s 
			    GROUP BY aj.id,aj.name
			""", (tuple(st_line_ids),))
			payments = self.env.cr.fetchall()
			# payments = self.env.cr.dictfetchall()
			for x in payments:
				journals_pos.setdefault(x[0], [x[1], 0.0])
				journals_pos[x[0]][1] += x[2]

				totales_pay.setdefault(x[0], [x[1], 0.0])
				totales_pay[x[0]][1] += x[2]

		invoices = self.env['account.invoice'].sudo().search([
			('date_invoice', '>=', date_start),
			('date_invoice', '<=', date_stop),
			('user_id', 'in', users.ids),
			('state', 'not in', ['draft','cancel']),
			('type', '=', 'out_invoice')], order="user_id asc")

		total_i, tax_inv, total_inv, disc_inv = 0.0,0.0,0.0,0.0
		p_iniciales = 0.0
		taxes_inv = {}

		for inv in invoices:
			tax_inv += inv.amount_tax
			total_inv += inv.amount_total
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
			('payment_type', '=', 'inbound')], order="journal_id asc")

		journals_pay = {}
		journals_pay_inc = {}
		for pay in payments:
			bandera = False
			if 'hfoc_inicial' in pay._fields:
				if pay.hfoc_inicial:
					p_iniciales += pay.amount
					bandera = True
				else:
					bandera = False
			if bandera: #Iniciales
				journals_pay_inc.setdefault(pay.journal_id.id, [0.0, 0.0, 0.0, pay.journal_id.name])
				journals_pay_inc[pay.journal_id.id][0] += pay.amount
			else:
				if pay.invoice_ids: #Anticipos
					journals_pay_inc.setdefault(pay.journal_id.id, [0.0, 0.0, 0.0, pay.journal_id.name])
					journals_pay_inc[pay.journal_id.id][1] += pay.amount
				else: #Abono
					journals_pay_inc.setdefault(pay.journal_id.id, [0.0, 0.0, 0.0, pay.journal_id.name])
					journals_pay_inc[pay.journal_id.id][2] += pay.amount


			journals_pay.setdefault(pay.journal_id.id, [pay.journal_id.name, 0.0])
			journals_pay[pay.journal_id.id][1] += pay.amount
			totales_pay.setdefault(pay.journal_id.id, [pay.journal_id.name, 0.0])
			totales_pay[pay.journal_id.id][1] += pay.amount
		user_currency = self.env.user.company_id.currency_id

		return {
			'currency_precision': user_currency.decimal_places,
			'currency_id': user_currency,
			'count_pos': len(orders),
			'tax_pos' : tax_pos,
			'total_pos' : total_pos,
			'total_p' : total_p + disc_pos,
			'disc_pos' : disc_pos,
			'count_inv': len(invoices),
			'tax_inv' : tax_inv,
			'total_inv' : total_inv,
			'p_iniciales': p_iniciales,
			'total_i' : total_i + disc_inv,
			'disc_inv' : disc_inv,
			'journals' : journals_pay,
			'taxes_inv' : list(taxes_inv.values()),
			'taxes_pos' : list(taxes_pos.values()),
			'journals_pos' : list(journals_pos.values()),
			'journals_pay' : list(journals_pay.values()),
			'journals_pay_inc' : list(journals_pay_inc.values()),
			'totales_tax' : list(totales_tax.values()),
			'totales_pay' : list(totales_pay.values()),
			'user_ventas' : users,
		}



	@api.multi
	def _get_report_values(self, docids, data=None):
		data = dict(data or {})
		users = self.env['res.users'].browse(data['user_ids'])
		data.update(self.get_sale_details(data['date_start'], data['date_stop'], users))
		return data