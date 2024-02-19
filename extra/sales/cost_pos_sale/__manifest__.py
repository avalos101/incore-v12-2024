# -*- coding: utf-8 -*-
{
    'name': 'Report Cost POS sale',
    'summary': 'Report Cost POS sale',
    'version': '1.0',
    'category': 'Point Of Sale',
    'website': '',
    'author': '',
    'license': '',
    'application': False,
    'installable': True,
    'depends': [
        'point_of_sale', 
        'base',
        ],
    'description': '''

========================

''',    
    'data': [
        'security/ir.model.access.csv',
        'views/cost_pos_sale_view.xml',
    ],
    'qweb': [
    ]
}
