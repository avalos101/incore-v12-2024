# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import api, fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    team_type = fields.Selection(selection_add=[('ebay', 'eBay')])
