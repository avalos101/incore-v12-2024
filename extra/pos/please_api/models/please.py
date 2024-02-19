from incore import models, fields, _, api
from incore.addons.please_api.models.please_api import PleaseAPI
from incore.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class Please(models.Model):
	_name = "please"
	_description = "Please credentials"
	_rec_name = "name"

	name = fields.Char(string="Name", required=True)
	user = fields.Char(string="User", required=True)
	password = fields.Char(string="Password", required=True)
	company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)


	@api.multi
	def button_test(self):
		p = PleaseAPI(self.user, self.password)
		status = p.get_session()
		if status:
			raise UserError(_("Connection Test Succeeded! Everything seems properly set up!"))
		else:
			raise UserError(_("Connection Test Failed!"))