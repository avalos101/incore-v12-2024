# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models


class IrActionsServer(models.Model):
    _name = 'ir.actions.server'
    _inherit = ['studio.mixin', 'ir.actions.server']
