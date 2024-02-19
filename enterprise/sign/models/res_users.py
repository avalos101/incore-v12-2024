# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    sign_signature = fields.Binary(string="Digital Signature", attachment=True, groups="base.group_system")
    sign_initials = fields.Binary(string="Digitial Initials", attachment=True, groups="base.group_system")
