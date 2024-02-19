from incore import models, fields

class POSConfig(models.Model):
	_inherit = 'pos.config'

	print_kitchen_receipt = fields.Boolean(string="Print Kitchen Receipt")