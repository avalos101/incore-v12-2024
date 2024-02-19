# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.
from incore import api, fields, models, _
from incore.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_security_pin = fields.Char(string='Security PIN', size=32, help='A Security PIN used to protect sensible functionality in the Point of Sale')

    @api.constrains('pos_security_pin')
    def _check_pin(self):
        if self.pos_security_pin and not self.pos_security_pin.isdigit():
            raise UserError(_("Security PIN can only contain digits"))
