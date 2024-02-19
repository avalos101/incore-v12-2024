# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Float(help='The loyalty points the user won as part of a Loyalty Program')
