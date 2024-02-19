# -*- coding: utf-8 -*-

{
    'name': 'POS Receipt Merkasilver Custom',
    'version': '1.1.3',
    'category': 'Point Of Sale',
    'sequence': 21,
    'author': 'Gustavo H.',
    'summary': 'Impresion de ticket desde el pedido del POS.',
    'description': """

=======================

Impresion de ticket del pedido de POS Merkasilver Custom.

""",
    'depends': ['point_of_sale','l10n_co_pos'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/pos_template.xml',
        'views/pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
}
