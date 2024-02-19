# -*- coding: utf-8 -*-
from incore import api, fields, models, SUPERUSER_ID, _

class PosConfig(models.Model):
	_inherit = 'pos.config'

	pos_tiket = fields.Selection(selection=[
		('default','Default'),('58mm','58 mm')],
		string=u'Tamaño ticket', default='default')
	pos_name_order = fields.Boolean(string="Mostrar codigo del Pedido")