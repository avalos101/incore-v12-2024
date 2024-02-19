# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    website_checkout_comments = fields.Text(
        'Message of customer',
        help='Additional message of customer on checout on ecommerce')
    website_checkout_gift = fields.Boolean(
        'Gift', help='The customer wants its order in a gift.')
    website_checkout_gift_msg = fields.Text('Message for gift')
    website_checkout_tandc = fields.Boolean(
        'Terms and Conditions',
        help='This indicates if the user accepted the terms and conditions.')
