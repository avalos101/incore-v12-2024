# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class QualityCheck(models.Model):
    _inherit = "quality.check"

    production_id = fields.Many2one('mrp.production', 'Production Order')


class QualityAlert(models.Model):
    _inherit = "quality.alert"

    production_id = fields.Many2one('mrp.production', "Production Order")
