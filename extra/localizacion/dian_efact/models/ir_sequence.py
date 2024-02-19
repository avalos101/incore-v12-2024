from incore import api, fields, models, _
from incore.exceptions import Warning
from incore.osv import osv

class ir_sequence(models.Model):
    _inherit = 'ir.sequence'

