# -*- encoding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2011 Noviat nv/sa (www.noviat.be). All rights reserved.

from incore import fields, models


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    coda_note = fields.Text('CODA Notes')


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    def _check_journal_bank_account(self, journal, account_number):
        if journal.bank_account_id.acc_type == 'iban' and journal.bank_account_id.get_bban() == account_number:
            return True
        return super(AccountBankStatementImport, self)._check_journal_bank_account(journal, account_number)
