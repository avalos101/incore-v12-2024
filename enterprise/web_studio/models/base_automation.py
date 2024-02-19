# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models


class BaseAutomation(models.Model):
    _name = 'base.automation'
    _inherit = ['studio.mixin', 'base.automation']
