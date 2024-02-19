# -*- coding: utf-8 -*-
###################################################################################

{
    'name': 'Informe Consolidado de Ventas',
    'version': '1.0.1',
    'category': 'Pint of Sale',
    'summary': "Modulo de informe de peidos, facturas y pagos",
    'author': 'Gustavo H.',
    'company': 'BEANSOFT.SRL',
    'website': 'http://www.iaben.com',
    'description': """

Informe de Consolidado de Ventas por Cajero(s)
=======================
""",
    'depends': ['point_of_sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_sale_invoice_wiz.xml',
        'views/report_inv_so.xml',
        'views/report.xml',
    ],
    'demo': [
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
