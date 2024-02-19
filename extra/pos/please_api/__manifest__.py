# -*- coding: utf-8 -*-
{
    'name': 'Integration please API',
    'version': '1.0.0',
    'category': 'Point Of Sale',
    'author': 'Gustavo H.',
    'summary': 'Integracion de pedidos con PLEASE API',
    'depends': ['base', 'base_address_city', 'point_of_sale'],
    'data': [
        "data/res.city.csv",
        "data/res_country.xml",
        "security/ir.model.access.csv",
        "views/account_journal_view.xml",
        "data/account_journal.xml",
        "views/please_api_views.xml",
        "views/please_views.xml",
        "views/pos_order_view.xml",
        "views/menu_please.xml",
        "template/template.xml",
        "data/please_cron.xml"
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
