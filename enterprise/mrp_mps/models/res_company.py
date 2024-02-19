# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class Company(models.Model):
    _inherit = "res.company"

    manufacturing_period = fields.Selection([
        ('month', 'Monthly'),
        ('week', 'Weekly'),
        ('day', 'Daily')], string="Manufacturing Period",
        default='month', required=True,
        help="Default value for the time ranges in Master Production Schedule report.")
