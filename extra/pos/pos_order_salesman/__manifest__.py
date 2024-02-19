# -*- coding: utf-8 -*-
{
    'name': "POSVendedores",
    'version': '12.0.1.0.0',
    'summary': """ Helps the salesman to specify the salesman""",
    'author': "Diego Avalos",
    'category': 'Point of Sale',
    'depends': ['pos_restaurant', 'point_of_sale'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'security/ir.model.access.csv'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
