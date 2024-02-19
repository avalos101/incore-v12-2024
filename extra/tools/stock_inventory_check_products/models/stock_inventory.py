# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import models, _
from incore.exceptions import ValidationError


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    def action_validate(self):
        products_checked = all(self.mapped('line_ids.product_check'))
        if not products_checked:
            raise ValidationError(_('You must check all products'))
        return super().action_validate()
