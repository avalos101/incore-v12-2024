# -*- coding: utf-8 -*-


{
    'name': "Cancel Sale And Purchase Order With Related Pickings and Invoices",
    'version': "12.0.0.0",
    'summary': "This module used to Cancel Sales and Purchase orders with related invoices and pickings",
    'category': 'Warehouse',
    'description': """
    cancel Sales order
    cancel sale order with invoice
    cancel sale order with related picking
    cancel purchase order
    cancel purchase order with related picking
    cancel quotation
    cancel rfq
    cancel request for quotation



    """,
    'author': "inCore",
    'depends': ['base','stock','sale_management','purchase','sr_stock_picking_cancel'],
    'data': [
    ],
    'images': ['static/description/banner.png'],
    "price": 5,
    "currency": 'EUR',
    'demo': [],
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
}
