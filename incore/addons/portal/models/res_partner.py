# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def can_edit_vat(self):
        return True
