# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'POS PriceList (Enterprise)',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary' : "Point of Sale PriceList",
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "www.acespritech.com",
    'depends': ['web', 'point_of_sale','sale'],
    'price': 15,
    'currency': 'EUR',
    'images': ['static/description/2.pos_config.png'],
    'data': [
        'views/pos_pricelist_aces.xml',
    ],
    'demo': [],
    'test': [],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: