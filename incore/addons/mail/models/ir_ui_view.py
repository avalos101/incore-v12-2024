# -*- coding: utf-8 -*-
from incore import fields, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('activity', 'Activity')])
