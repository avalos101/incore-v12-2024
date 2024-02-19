# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models, fields


class Users(models.Model):
    _inherit = 'res.users'
    incorebot_state = fields.Selection(
        selection_add=[
            ('onboarding_canned', 'Onboarding canned'),
        ])
