# -*- coding: utf-8 -*-
{
    'name': 'POS Default Customer',
    'summary': "Set Default Customer in POS",
    'description': 'Set Default Customer in POS',

    'author': 'inCore',

    'category': 'Point of Sale',
    'version': '12.0.0.1.0',
    'depends': ['point_of_sale'],

    'data': [
        'views/assets.xml',
        'views/pos_config_view.xml',
    ],

    'license': "OPL-1",

    'installable': True,
    'application': True,
}
