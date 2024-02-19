# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
{
    'name' : 'POS Quick Access',
    'version' : '12.1.0',
    'summary': 'Access POS by Some Quick Actions.',
    'author': "WeR Informative",
    'category': 'Point of Sale',
    'description': """
    By This Module User Will Allowed to Create Customer, Product and 
    Change View of Product List, Clear Cart by Single Click.
""",
    'website': 'https://werinformative.com/',
    'price': 15.00, 
    'currency': 'EUR',
    'depends' : ['base','point_of_sale'],
    "data": [
        'views/pos_config_view.xml',
        'views/wer_pos_quick_access.xml'
    ],
    'images': ['static/description/screenshots/banner.png'],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
