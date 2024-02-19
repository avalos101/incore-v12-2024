# -*- coding: utf-8 -*-


{
    'name': "Stock Picking Cancel",
    'version': "12.0.0.0",
    'summary': "This module used to Cancel Incoming and Outgoing Shipment/picking",
    'category': 'Warehouse',
    'description': """
    cancel stock picking
    cancel incoming shipment
    cancel outgoing shipment
    cancel internal shipment
    cancel stock
    cancel delivery
    cancel shipment
    revert shipment
    revert delivery



    """,
    'author': "inCore",
    'depends': ['base','stock'],
    'data': [
        'views/inherited_stock_picking.xml'
    ],
    'images': ['static/description/banner.png'],
    "price": 10,
    "currency": 'EUR',
    'demo': [],
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
}
