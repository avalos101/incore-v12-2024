# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    background_image = fields.Binary(string="Home Menu Background Image", attachment=True)
