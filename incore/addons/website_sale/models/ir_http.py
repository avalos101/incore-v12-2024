# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.
from incore import models
from incore.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        affiliate_id = request.httprequest.args.get('affiliate_id')
        if affiliate_id:
            request.session['affiliate_id'] = int(affiliate_id)
        return super(IrHttp, cls)._dispatch()
