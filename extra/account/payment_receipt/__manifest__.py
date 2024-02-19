# -*- coding: utf-8 -*-

{
    'name': 'Payment Receipt',
    'version': '1.0',
    'category': 'Account',
    'sequence': 6,
    'author': 'Avalos',
    'summary': 'Payment receipt module allows you to print Payment in receipt.',
    'description': """

=======================

Payment receipt module allows you to print Payment in receipt

""",
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        # 'static/src/xml/pos.xml',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
}
