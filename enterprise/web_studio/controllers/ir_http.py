# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models
from incore.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()

        if result['is_system']:
            # necessary keys for Studio
            result['dbuuid'] = request.env['ir.config_parameter'].sudo().get_param('database.uuid')
            result['multi_lang'] = bool(request.env['res.lang'].search_count([('code', '!=', 'en_US')]))

        return result
