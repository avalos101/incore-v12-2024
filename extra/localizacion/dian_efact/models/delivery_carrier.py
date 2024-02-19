from incore import api, fields, models, _
from incore.exceptions import Warning
from incore.osv import osv

class delivery_carrier(models.Model):
    _name = "delivery.carrier"
    _inherit = "delivery.carrier"

    nit = fields.Char('NIT', required=False, translate=True)