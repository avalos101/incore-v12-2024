# -*- coding: utf-8 -*-

{
    'name': 'Account Invoice Receipt',
    'version': '1.1.0',
    'category': 'Account',
    'sequence': 6,
    'author': 'Webveer',
    'summary': 'Account Invoice receipt module allows you to print Account order receipt.',
    'description': """

=======================

Account Invoice receipt module allows you to print account order receipt.

""",
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        # 'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/receipt.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'currency': 'EUR',
}
