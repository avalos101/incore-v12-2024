from incore import models, fields, api, _
from incore.addons.please_api.models.please_api import PleaseAPI
import logging
_logger = logging.getLogger(__name__)

class PleaseOrder(models.Model):
	_name = "please.order"
	_description = "History simpli order"
	_order = "order_number desc"
	_rec_name = "order_number"

	# @api.depends('order_status.event_type')
	# def _status_tracking(self):
	# 	for order in self:
	# 		st_track = order.order_status.sorted(lambda x: x.date)
	# 		order.state_tracking = st_track and st_track[-1].event_type or 'Ninguno'

	@api.model
	def _get_selection_tracking(self):
		selection = [
			("A_PENDING", "Pendiente"),
			("B_INTRANSPORT", "En transporte"),
			("C_DELIVERED", "Entregado"),
			("D_RETURN", "Devolución"),
			("E_ISSUE", "Novedad"),
			("F_CANCELED", "Cancelado")
		]
		return selection

	order_number = fields.Char(string='Order Number', required=True)
	storeId = fields.Char(string="Store ID")
	container_number = fields.Char(string="Container Number")
	sticker = fields.Boolean(string="Sticket", default=False)
	company_id = fields.Many2one('res.company', string="Company")
	currency_id = fields.Many2one('res.currency', string="Currency")
	total_price = fields.Float(string='Total', required=True, currency_field="currency_id")
	shipping_address = fields.Char(string="Shipping Address", required=True)
	city_id = fields.Many2one('res.city', string='City', required=True)
	cust_email = fields.Char(string="Email")
	partner_id = fields.Many2one('res.partner',string="Customer", required=True)
	cust_phone = fields.Char(string="Phone", required=True)
	cust_note = fields.Char(string="Note")
	cash_in_delivery = fields.Boolean(string="Payment on delivery", default=False)
	order_lines = fields.One2many('please.order.line', 'order_id', string="Detail")
	order_status = fields.One2many('please.order.state', 'order_id', string="Order Status")
	tracking = fields.Char(string="Response")
	state = fields.Selection(selection=[('draft','Draft'),('sent','Sent')], string="Status", default="draft")
	state_tracking = fields.Selection(selection=_get_selection_tracking, string="State Tracking", default='A_PENDING')
	# state_tracking = fields.Char(compute='_status_tracking', string="State Tracking", store=True, readonly=True)
	please_id = fields.Many2one('please', string="Credentials")

	@api.multi
	def action_send(self):
		if self.state == 'draft':
			self._cron_please_order()

	@api.model
	def _cron_please_order(self):
		if self:
			please_order = self
		else:
			please_order = self.search([('state','=','draft')], order="order_number asc")
		for po in please_order:
			p = PleaseAPI(po.please_id.user, po.please_id.password)
			values, lines = self._prepare_please_order_send(po, p)
			res = p.create_so(values, lines)
			if res:
				po.tracking = "%s" %res
				po.state = 'sent'

	def _prepare_please_order_send(self, po, p):
		values = {
			'storeOrderNumber': po.order_number,
			'totalPrice': po.total_price,
			'shippingAddress': po.shipping_address,
			'city': po.city_id.name,
			'customerName': po.partner_id.name,
			'customerPhoneNumber': po.cust_phone,
			'customerNote': po.cust_note,
			'cashOnDelivery': po.cash_in_delivery,
			'customerEmail': po.partner_id.email,
			'sticker': po.sticker,
			'ContainerNumber': po.container_number,
		}
		##### Esta por verse ya que no se comprende como va a funcionar
		# please = self.env['please'].search([])
		# if len(please.ids) > 1:
		# 	store = p.get_stores()
		# 	values.update({
		# 		'storeId': store[0].get('id'),
		# 		})
		lines = []
		for l in po.order_lines:
			line = {
				'name':l.name ,
				'quantity': l.quantity,
				'price': l.price
			}
			lines.append(line)
		return values, lines

	@api.multi
	def action_get_tracking(self):
		if self.state_tracking in ["A_PENDING","B_INTRANSPORT"]:
			self._cron_please_tracking()

	@api.model
	def _cron_please_tracking(self):
		if self:
			please_tracking = self
		else:
			please_tracking = self.search([
				('state','=','sent'),
				('state_tracking','in', ["A_PENDING","B_INTRANSPORT"])], order="order_number asc")

		for po in please_tracking:
			p = PleaseAPI(po.please_id.user, po.please_id.password)
			######### Pendiente
			# if p.sticker:
			# 	track = (po.tracking).split('?Order=')
			# else:
			# 	track = (po.tracking).split('?g=')
			track = po.order_number
			state_track = p.get_tracking_state(track)
			_logger.info('\n\n %r \n\n', state_track)
			if state_track:
				po.write({"state_tracking": state_track.get('statusType')}) 
			res = p.get_traking_so(track)
			values = self._create_please_tracking(res, po)
			if values:
				po.write({'order_status': values})

	def _create_please_tracking(self, response, po):
		states = []
		if response and len(po.order_status) < len(response):
			for trk in response[len(po.order_status):]:
				value = {
					# "order_id": po.id,
					"id_ref": trk.get("id"),
					"date": trk.get("date"),
					"created_by": trk.get("createdBy"),
					"event_type": trk.get("eventType"),
					"event_name": trk.get("eventName"),
					"notes": trk.get("notes")
				}
				states.append([0,0,value])
		return states

class PleaseOrderLine(models.Model):
	_name = "please.order.line"
	_description = "Simpli order detail"

	order_id = fields.Many2one('please.order', string="Order", required=True, ondelete='cascade')
	name = fields.Char(string="Name", required=True)
	quantity = fields.Integer(string="Quantity", required=True)
	price = fields.Float(string="Price", readonly=True)

class PleaseOrderStatus(models.Model):
	_name = "please.order.state"
	_description = "Simpli order status"
	_order = "date desc"

	order_id = fields.Many2one('please.order', string="Order", required=True, ondelete='restrict')
	id_ref = fields.Char(string="Id response")
	date = fields.Datetime(string="Date", help=u"Fecha del evento")
	created_by = fields.Char(string="User", help=u"Usuario que generó el evento en el sistema de Please")
	event_type = fields.Char(string="Event type", help=u"Tipo de evento")
	event_name = fields.Char(string="Event name", help=u"Nombre del evento")
	notes = fields.Char(string="Note", help=u"Información adicional (opcional)")