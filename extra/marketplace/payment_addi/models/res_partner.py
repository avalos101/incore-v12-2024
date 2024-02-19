from incore import fields, models, api, _

class Partner(models.Model):
	_inherit = "res.partner"

	last_name = fields.Char(string="Apellido")