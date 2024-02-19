# -*- coding: utf-8 -*-

from incore import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'


    def mobile_whatsapp_link(self):
        for rec in self:
            if rec.mobile:
                return {
                    'type': 'ir.actions.act_url',
                    'url': "https://web.whatsapp.com/send?phone=" + rec.mobile or "https://api.whatsapp.com/send?phone=" + rec.mobile,
                    'target': 'new',
                    'res_id': rec.id,
                }
