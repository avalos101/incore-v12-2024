from incore import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
	_inherit = "pos.order"

	order_please_id = fields.Many2one('please.order', string="Please order")
	to_please = fields.Boolean(string="Please", default=False)

	@api.model
	def _order_fields(self, ui_order):
		fields = super(PosOrder, self)._order_fields(ui_order)
		fields['note'] = ui_order.get('note', False)
		return fields

	@api.model
	def _process_order(self, pos_order):
		res = super(PosOrder, self)._process_order(pos_order)
		self._create_please(res, pos_order)
		return res

	@api.model
	def _create_please(self, order, pos_order):
		if pos_order['to_please']:
			vals = self._prepare_please_order(order, pos_order)
			order_please = self.env['please.order'].create(vals)
			order.order_please_id = order_please.id

	@api.model
	def _prepare_please_order(self, order, pos_order):
		cash_in_delivery = order.statement_ids.filtered(lambda stm: stm.journal_id.upon_delivery) or False
		vals = {
			"order_number" : order.name,
			"container_number" : order.name,
			"sticker" : False,
			"company_id" : order.company_id.id,
			"currency_id" : order.pricelist_id.currency_id.id,
			"total_price" : cash_in_delivery and cash_in_delivery.amount or order.amount_total,
			"shipping_address" : order.partner_id.street,
			"city_id" : order.partner_id.city_id.id,
			"cust_email" : order.partner_id.email or False, #optional
			"partner_id" : order.partner_id.id,
			"cust_phone" : order.partner_id.phone,
			"cust_note" : order.note, #optional
			"cash_in_delivery" : cash_in_delivery and True or False,
			"order_lines" : [],
			"state" : 'draft',
			"please_id" : order.session_id.config_id.please_id.id,
		}
		for l in order.lines:
			lines = {
				"name": l.product_id.product_tmpl_id.name,
				"quantity": int(l.qty),
				"price": l.price_unit,
			}
			vals['order_lines'].append((0,0,lines))

		return vals