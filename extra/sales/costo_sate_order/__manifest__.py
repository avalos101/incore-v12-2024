# -*- coding: utf-8 -*-


{
    'name': 'Costo de Venta',
    'summary': """
    Costo de Venta en reporte de Ventas Pivot
    """,
    "version": '0.0.2',
    'category': 'Sales',
    'author': 'Gustavo H.',
    'license': 'AGPL-3',
    'sequence': 4,
    'installable': True,
    'auto_install': False,
    'application': True,
    'description': """
        Costo de Venta en reporte de Ventas Pivot
    """,
    'depends':[
        'sale',
        'sale_management',
    ],
    'data':[
        'views/sale_cost_view.xml.xml',
        'data/sale_costo.xml'
        ],
    'demo':['data/sale_cost_demo.xml'],
}
