# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def get_website_sale_document_types(self):
        model_fields = self.fields_get(['doctype'])
        document_type_selection = dict(
            model_fields['doctype']['selection'])
        return document_type_selection

    @api.model
    def website_sale_compute_nit(self, xidentification):
        """Get NIT computed for pass it to the website."""
        dummy_partner = self.env['res.partner'].new({
            'xidentification': xidentification,
            'doctype': 31,
        })
        nit_formatted = dummy_partner.formatedNit
        return nit_formatted
