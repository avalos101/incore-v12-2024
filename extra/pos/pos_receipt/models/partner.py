# coding: utf-8

from incore import models, api

class Partner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def select_in_pos_current_order(self):
        res = super(Partner, self).select_in_pos_current_order()
        res['payload'].update({'cedula': self.xidentification or ''})
        return res
