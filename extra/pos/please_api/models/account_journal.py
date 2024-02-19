from incore import fields, models, api, _

class AccountJournal(models.Model):
	_inherit = "account.journal"

	upon_delivery = fields.Boolean(string="upon delivery", default=False)