# -*- coding: utf-8 -*-	
# Part of inCore. See LICENSE file for full copyright and licensing details.	

from incore import fields, models	


class ResConfigSettings(models.TransientModel):	
    _inherit = 'res.config.settings'	

    snailmail_color = fields.Boolean(string='Print In Color', related='company_id.snailmail_color', readonly=False)
    snailmail_duplex = fields.Boolean(string='Print Both sides', related='company_id.snailmail_duplex', readonly=False)
