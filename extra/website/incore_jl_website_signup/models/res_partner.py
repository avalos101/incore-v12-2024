# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    auth_data_processing = fields.Boolean(
        'Accepted Data Processing',
        help='Indicates the user accepted the data processing in the signup.')

    @api.constrains('doctype', 'xidentification')
    def _checkDocType(self):
        """
        This function throws and error if there is no document type selected.
        @return: void
        """
        if not self.env.context.get('partner_from_signup'):
            super()._checkDocType()

    @api.model
    def website_get_email(self, doctype, xidentification):
        """Returns email found for document received."""
        found = self.sudo().search([
            ('xidentification', '=', xidentification),
            ('doctype', '=', doctype),
        ])
        if found:
            return found[0].email
        else: return False
