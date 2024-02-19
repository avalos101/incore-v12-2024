from incore import fields, models, api, _

class PosConfig(models.Model):
	_inherit = "pos.config"

	please_id = fields.Many2one('please', string="User Please")
