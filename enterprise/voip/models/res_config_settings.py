# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
from incore import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wsServer = fields.Char("WebSocket", help="The URL of your WebSocket",
                           default='ws://localhost', config_parameter='voip.wsServer')
    pbx_ip = fields.Char("PBX Server IP", help="The IP adress of your PBX Server",
                         default='localhost', config_parameter='voip.pbx_ip')
    mode = fields.Selection([
        ('demo', 'Demo'),
        ('prod', 'Production'),
    ], string="VoIP Environment", default='demo', config_parameter='voip.mode')
