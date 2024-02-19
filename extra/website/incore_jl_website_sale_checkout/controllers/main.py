# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import http, _
from incore.http import request
from incore.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route()
    def address(self, **kw):
        res = super().address(**kw)
        order = request.website.sale_get_order()
        if 'submitted' in kw and order:
            gift = True if kw.get('website_checkout_gift') == '1' else False
            accept_tandc = (True if kw.get('website_checkout_tandc') == '1'
                            else False)
            gift_msg = kw.get('website_checkout_gift_msg')
            if not gift:
                gift_msg = False
                
            order.write({
                'website_checkout_comments': kw.get(
                    'website_checkout_comments'),
                'website_checkout_gift': gift,
                'website_checkout_gift_msg': gift_msg,
                'website_checkout_tandc': accept_tandc,
            })

        document_type = request.env.user.doctype
        document_types = request.env[
            'res.partner'].get_website_sale_document_types()
        res.qcontext.update({
            'document_type': document_type,
            'document_types': document_types,
        })
        return res

    def _get_mandatory_billing_fields(self):
        required_fields = super()._get_mandatory_billing_fields()
        if 'city' in required_fields:
            required_fields.remove('city')
        if 'name' in required_fields:
            required_fields.remove('name')
        required_fields.append('doctype')
        required_fields.append('xidentification')
        required_fields.append('xbirthday')
        required_fields.append('x_lastname1')
        required_fields.append('x_name1')
        required_fields.append('phone')
        return required_fields

    def _get_mandatory_shipping_fields(self):
        required_fields = super()._get_mandatory_shipping_fields()
        if 'city' in required_fields:
            required_fields.remove('city')
        if 'name' in required_fields:
            required_fields.remove('name')
        return required_fields

    def values_preprocess(self, order, mode, values):
        res = super().values_preprocess(order=order, mode=mode, values=values)
        if res.get('city') and res.get('country_id') and res.get('state_id'):
            res_country_state_city = request.env['res.country.state.city']
            city = res_country_state_city.search([
                ('country_id', '=', int(res['country_id'])),
                ('state_id', '=', int(res['state_id'])),
                ('name', 'ilike', res['city']),
            ])
            if city:
                res['xcity'] = city[0].id

        name = ''
        if res.get('x_name1'):
            name += res['x_name1']
        if res.get('x_name2'):
            name += ' %s' % res['x_name2']
        if res.get('x_lastname1'):
            name += ' %s' % res['x_lastname1']
        if res.get('x_lastname2'):
            name += ' %s' % res['x_lastname2']
        res['name'] = name
        return res

    @http.route(['/shop/checkout/get_nit_formatted'], type="json", auth="public", website=True)
    def get_nit_formatted(self, xidentification):
        """Get NIT computed for pass it to the website."""
        json_dict = {}
        json_dict['nit_formatted'] = request.env[
            'res.partner'].website_sale_compute_nit(xidentification)
        return json_dict

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode=mode, all_form_values=all_form_values, data=data)

        if (data.get('doctype') and data.get('xidentification')
                and data.get('partner_id')):
            res_partner = request.env['res.partner']
            partner_exists = res_partner.sudo().search([
                ('doctype', '=', int(data['doctype'])),
                ('xidentification', '=', data['xidentification']),
                ('id', '!=', int(data['partner_id'])),
            ])
            if partner_exists:
                error['xidentification'] = 'error'
                error_message.append(_(
                    'Invalid document! This document already exists for other customer/contact.'))
        return error, error_message
