# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.

import logging
from incore import api, fields, models, tools, _
_logger = logging.getLogger(__name__)

class product_template(models.Model):
	_inherit = 'product.template'

	margen = fields.Float('Margen (%)', default=0.0)

	@api.onchange('margen','standard_price')
	def change_margin_cost(self):
		if self.margen != 0 and self.standard_price != 0.0:
			self.list_price = round(self.standard_price + (self.standard_price * ((self.margen or 0.0)/100.0)),-3)

	@api.multi
	def write(self, vals):
		if 'standard_price' in vals:
			if self.margen != 0.0:
				vals['list_price'] = round(vals['standard_price'] + (vals['standard_price'] * ((self.margen or 0.0)/100.0)),-3)
		return super(product_template, self).write(vals)

class product_product(models.Model):
	_inherit = 'product.product'

	@api.multi
	def write(self, vals):
		if 'standard_price' in vals:
			if self.margen != 0.0:
				vals['list_price'] = round(vals['standard_price'] + (vals['standard_price'] * ((self.margen or 0.0)/100.0)),-3)
		return super(product_product, self).write(vals)
