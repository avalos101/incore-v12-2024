# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import fields, models


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    product_check = fields.Boolean('OK')
