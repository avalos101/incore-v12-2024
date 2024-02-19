# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    days_between_two_followups = fields.Integer(string='Number of days between two follow-ups', default=14)
    totals_below_sections = fields.Boolean(
        string='Add totals below sections',
        help='When ticked, totals and subtotals appear below the sections of the report.')