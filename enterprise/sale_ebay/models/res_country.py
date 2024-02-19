# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models, fields


class ResCountry(models.Model):
    _inherit = "res.country"

    ebay_available = fields.Boolean("Availability To Use For eBay API", readonly=True)
