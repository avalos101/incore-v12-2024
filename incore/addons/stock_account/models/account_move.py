# -*- coding: utf-8 -*-

from incore import fields, models, _

from incore.tools.float_utils import float_is_zero

from incore.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    stock_move_id = fields.Many2one('stock.move', string='Stock Move')
