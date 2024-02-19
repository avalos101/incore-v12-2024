# -*- coding: utf-8 -*-

from incore import api, fields, models, tools, _


class Company(models.Model):
    _inherit = "res.company"

    ref = fields.Char(related='partner_id.ref', store=False)

