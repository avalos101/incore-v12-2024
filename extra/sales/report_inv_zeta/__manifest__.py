# -*- coding: utf-8 -*-
###################################################################################

{
    'name': 'Informe Factura Z',
    'version': '1.0.0',
    'category': 'Account',
    'summary': "Modulo de informe de reporte Z de Facturacion",
    'author': 'Gustavo H.',
    'company': 'BEANSOFT.SRL',
    'website': 'http://www.iaben.com',
    'description': """

Informe de Factura Z  por Cajero(s)
=======================
""",
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_invoice_wiz.xml',
        'views/report_inv.xml',
        'views/report.xml',
    ],
    'demo': [
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
