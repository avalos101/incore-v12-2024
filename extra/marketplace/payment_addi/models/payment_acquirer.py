# -*- coding: utf-'8' "-*-"

import requests
import json

from ast import literal_eval
from incore import api, models, fields
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('addi', 'ADDI')]
    )
    addi_api_key = fields.Char(
        string="Api Key",
    )
    addi_private_key = fields.Char(
        string="Secret Key",
    )

    @api.multi
    def _get_feature_support(self):
        res = super(PaymentAcquirer, self)._get_feature_support()
        res['fees'].append('addi')
        return res

    @api.model
    def _get_addi_urls(self, environment):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if environment == 'prod':
            return {
                'addi_form_url': base_url + '/payment/addi/redirect',
                'addi_url': "https://auth.addi.com",
                'addi_api': "https://api.addi.com",
                'addi_ecomer': "https://api.addi.com",
            }
        else:
            return {
                'addi_form_url': base_url + '/payment/addi/redirect',
                'addi_url': "https://auth.addi-staging.com",
                'addi_api': "https://api.staging.addi.com",
                'addi_ecomer': "https://api.addi-staging.com",
            }

    @api.multi
    def addi_get_form_action_url(self):
        return self._get_addi_urls(self.environment)['addi_form_url']

    def addi_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        reference = values['reference'].split('-')[0]
        order_id = self.env['sale.order'].search([('name', '=', reference)])
        items = []
        for line in order_id.order_line:
            # Ensamblamos los valores del producto
            product = {
                'sku': line.product_id.default_code,
                'name': line.product_id.name,
                'quantity': str(int(line.product_uom_qty)),
                'unitPrice': int(line.price_unit),
                'tax': int(line.price_tax),
                # "pictureUrl": "",
                # "category": ""
            }
            items.append(product)
        # 'orderId': order_id.name,
        values.update({
            'orderId': values['reference'],
            'totalAmount': str(values['amount']),
            'shippingAmount': "0.0",
            'totalTaxesAmount': str(order_id.amount_tax),
            'currency': values['currency'],
            'items': items,
            'client': {
                'idType': 'CC',
                'idNumber': str(values['partner'].vat),
                'firstName': values['partner'].name,
                'lastName': values['partner'].last_name,
                'email': values['partner'].email,
                'cellphone': str(values['partner'].phone),
                'cellphoneCountryCode': '+57',
                'address': {
                    'lineOne': values['partner'].street,
                    'city': values['partner'].city,
                    'country': values['partner'].country_id.code,
                }
            },
            'allyUrlRedirection': {
                'callbackUrl': base_url + '/payment/addi/notify',
                'redirectionUrl': base_url + '/payment/addi/return',
            },
            'acquirer_id': self.id,
        })
        _logger.info('\n\n %r \n\n', values)
        return values

    # def _addi_form_validate(self, data):
    #     codes = {
    #             '0': 'Transacción aprobada.',
    #             '-1': 'Rechazo de transacción.',
    #             '-2': 'Transacción debe reintentarse.',
    #             '-3': 'Error en transacción.',
    #             '-4': 'Rechazo de transacción.',
    #             '-5': 'Rechazo por error de tasa.',
    #             '-6': 'Excede cupo máximo mensual.',
    #             '-7': 'Excede límite diario por transacción.',
    #             '-8': 'Rubro no autorizado.',
    #         }
    #     status = data
    #     _logger.info("\n\ndata:{}\n\n".format(data))
    #     return True

    def addi_initTransaction(self, post):
        data = {
            "audience": self._get_addi_urls(self.environment)['addi_api'],
            "grant_type": "client_credentials",
            "client_id": self.addi_api_key,
            "client_secret": self.addi_private_key,
        }
        url = self._get_addi_urls(self.environment)['addi_url']
        token_request = requests.post(url + '/oauth/token', data=data)
        # Meter la validación
        token_values = json.loads(token_request.text)
        header = {
            'Authorization': 'Bearer ' + token_values['access_token'],
            "Content-Type": "application/json"
        }

        del post['acquirer_id']

        post['items'] = literal_eval(post['items'])
        post['client'] = literal_eval(post['client'])
        post['allyUrlRedirection'] = literal_eval(post['allyUrlRedirection'])

        transaction_request = requests.post(self._get_addi_urls(self.environment)['addi_ecomer']+'/v1/online-applications', headers=header,
                                            data=json.dumps(post), allow_redirects=False)
        return transaction_request.headers['Location']
