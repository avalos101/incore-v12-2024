# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models


class IrRule(models.Model):
    _name = 'ir.rule'
    _description = 'Rule'
    _inherit = ['studio.mixin', 'ir.rule']
