# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import api, fields, models
from incore.osv import expression


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _get_translation_frontend_modules_domain(cls):
        domain = super(IrHttp, cls)._get_translation_frontend_modules_domain()
        return expression.OR([domain, [('name', '=', 'im_livechat')]])

