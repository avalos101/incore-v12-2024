# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    resource_ids = fields.One2many(
        'resource.resource', 'user_id', 'Resources')
    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Default Working Hours',
        related='resource_ids.calendar_id', readonly=False)
