# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wsServer = fields.Char(default='wss://edge.sip.onsip.com', config_parameter='voip.wsServer')
