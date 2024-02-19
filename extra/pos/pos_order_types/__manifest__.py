# -*- coding: utf-8 -*-
{
    'name': "POS Order Types",
    'version': '12.0.1.0.0',
    'summary': """ Helps the salesman to specify the type of order like parcel, delivery etc.""",
    'description': """This module helps to choose the order types in POS screen. You have the option to choose 
                        different order types for multiple Point of Sale.""",
    'author': "Cybrosys Techno Solutions",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'category': 'Point of Sale',
    'depends': ['pos_restaurant', 'point_of_sale'],
    'website': 'http://www.cybrosys.com',
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'security/ir.model.access.csv'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'price': 9.99,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
}
