# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.

from incore import api, SUPERUSER_ID

from . import models
from . import wizard
from . import controllers
from . import report

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['product.template'].search([
        ('service_type', '=', 'timesheet')
    ]).write({'service_type': 'manual'})
    env['product.product'].search([
        ('service_type', '=', 'timesheet')
    ]).write({'service_type': 'manual'})
