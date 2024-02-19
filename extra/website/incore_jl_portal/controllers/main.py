# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore.addons.portal.controllers.portal import CustomerPortal
from incore.http import request, route

class CustomerPortal(CustomerPortal):

    @route()
    def account(self, redirect=None, **post):
        if 'name' in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.remove('name')
        if 'city' in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.remove('city')
        if 'x_name1' not in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.append('x_name1')
        if 'x_name2' not in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.append('x_name2')
        if 'x_lastname1' not in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.append('x_lastname1')
        if 'x_lastname2' not in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.append('x_lastname2')
        if 'doctype' not in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.append('doctype')
        if 'xidentification' not in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.append('xidentification')

        if 'name' not in self.OPTIONAL_BILLING_FIELDS:
            self.OPTIONAL_BILLING_FIELDS.append('name')
        if 'formatedNit' not in self.OPTIONAL_BILLING_FIELDS:
            self.OPTIONAL_BILLING_FIELDS.append('formatedNit')
        if 'city' not in self.OPTIONAL_BILLING_FIELDS:
            self.OPTIONAL_BILLING_FIELDS.append('city')
        response = super().account(redirect=redirect, **post)

        document_type = request.env.user.doctype
        document_types = request.env[
            'res.partner'].get_website_sale_document_types()
        response.qcontext.update({
            'document_type': document_type,
            'document_types': document_types,
        })

        return response

