from incore import api, fields, models, _
from incore.exceptions import Warning
from incore.osv import osv
import json
import os

class stock_picking(models.Model):
    _inherit = 'stock.picking'
    api_message = fields.Text(name="api_message", string="Estado", default='Documento contable sin emitir.')
