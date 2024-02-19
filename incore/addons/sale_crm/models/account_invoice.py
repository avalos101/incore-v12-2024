# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.

from incore import models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ['account.invoice', 'utm.mixin']
