from incore import api, fields, models, _
from incore.exceptions import Warning
from incore.osv import osv

class ir_cron(models.Model):
    _inherit = 'ir.cron'

    dian_start_date = fields.Date(string="Desde la fecha", name="dian_start_date")