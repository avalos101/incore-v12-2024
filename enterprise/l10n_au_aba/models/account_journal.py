# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import api, fields, models, _

from incore.exceptions import ValidationError

import re

class AccountJournal(models.Model):
    _inherit = "account.journal"

    aba_fic = fields.Char(string='Financial Institution Code', help='3 Character Financial Institution Code (e.g WBC for Westpac')
    aba_user_spec = fields.Char(string='Supplying User Name', help="Name of User supplying file - Your Financial Institution may specify the required User PreferredSpecification.")
    aba_user_number = fields.Char(string='APCA Identification Number', help='User Identification Number, allocated by APCA.')
    aba_self_balancing = fields.Boolean(string='Include Self Balancing Transaction', default=False)

    #Needed for "bank account" form, were the account number is directly set with a related field
    aba_bsb = fields.Char(string='BSB', related='bank_account_id.aba_bsb', help="BSB code of the account associated to this journal", readonly=False)

    @api.constrains('aba_fic')
    def _validate_aba_fic(self):
        """ FIC numbers must be 3 characters long, uppercase letters or digits.
        """
        for record in self:
            if record.aba_fic and not re.match("^(\d|[A-Z]){3}$", record.aba_fic):
                raise ValidationError(_('FIC is not valid (expected format is "XXX"). Please check with your Financial Institution.'))

    @api.constrains('aba_user_spec')
    def _validate_user_spec(self):
        for record in self:
            if record.aba_user_spec and len(record.aba_user_spec) > 26:
                raise ValidationError(_('User Specification Code cannot be longer than 26 characters. Please check with your Financial Institution.'))

    @api.constrains('aba_user_number')
    def _validate_user_number(self):
        """ ABA user number must consist of 6 digits.
        """
        for record in self:
            if record.aba_user_number and not re.match("^\d{6}$", record.aba_user_number):
                raise ValidationError(_('User number is not valid (expected format is "NNNNNN", only digits). Please check with your Financial Institution'))

    def _default_outbound_payment_methods(self):
        methods = super(AccountJournal, self)._default_outbound_payment_methods()
        return methods + self.env.ref('l10n_au_aba.account_payment_method_aba_ct')

    @api.model
    def _enable_aba_ct_on_bank_journals(self):
        """ Enables aba credit transfer payment method on bank journals. Called upon module installation via data file.
        """
        aba_ct = self.env.ref('l10n_au_aba.account_payment_method_aba_ct')
        aud = self.env.ref('base.AUD')
        if self.env.user.company_id.currency_id == aud:
            domain = ['&', ('type', '=', 'bank'), '|', ('currency_id', '=', aud.id), ('currency_id', '=', False)]
        else:
            domain = ['&', ('type', '=', 'bank'), ('currency_id', '=', aud.id)]
        for bank_journal in self.search(domain):
            bank_journal.write({'outbound_payment_method_ids': [(4, aba_ct.id, None)]})
