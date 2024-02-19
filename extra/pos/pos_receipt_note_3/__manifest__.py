# -*- coding: utf-8 -*-

{
    'name': 'POS Receipt Note',
    'version': '1.1.1',
    'category': 'Point Of Sale',
    'sequence': 22,
    'author': 'inCore Group S.A.S',
    'summary': 'Impresion de ticket desde el pedido del POS incluyendo la nota en el recibo',
    'description': """

=======================

Impresion de ticket del pedido de POS incluyendo la nota en el recibo.

""",
    'depends': ['point_of_sale','pos_restaurant','l10n_co_pos'],
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
