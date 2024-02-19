# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from . import models
from . import report
from . import wizard
from incore import api, SUPERUSER_ID


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['mail.activity.type'].search([
        ('category', '=', 'phonecall')
    ]).write({'category': 'default'})
