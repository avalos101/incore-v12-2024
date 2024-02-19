# -*- coding: utf-8 -*-

{
    'name': 'POS Receipt Las Cerezas',
    'version': '1.1.1',
    'category': 'Point Of Sale',
    'sequence': 21,
    'author': 'Gustavo H.',
    'summary': 'Impresion de ticket desde el pedido del POS.',
    'description': """

=======================

Impresion de ticket del pedido de POS.
Incluyendo la nota del perdido.
Version espeficica para las cerezas

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
