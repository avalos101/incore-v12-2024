# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models

class AccountAccount(models.Model):
    _inherit = 'account.account'

    in_tax_ids = fields.One2many('account.tax', 'account_id', copy=False)
