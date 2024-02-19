# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import api, models, modules


class Users(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']

    @api.model
    def systray_get_activities(self):
        """ Update the systray icon of ir.attachment activities to use the
        contact application one instead of base icon. """
        activities = super(Users, self).systray_get_activities()
        for activity in activities:
            if activity['model'] != 'ir.attachment':
                continue
            activity['icon'] = modules.module.get_module_icon('documents')
        return activities
