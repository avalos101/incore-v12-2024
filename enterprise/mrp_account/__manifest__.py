# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Accounting - MRP',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Analytic accounting in Manufacturing',
    'description': """
Analytic Accounting in MRP
==========================

* Cost structure report
""",
    'website': 'https://www.incore.co/page/manufacturing',
    'depends': ['mrp', 'stock_account'],
    'data': [
        'views/mrp_account_view.xml',
        'views/cost_structure_report.xml',
    ],
    'demo': ['demo/mrp_account_demo.xml'],
    'installable': True,
    'auto_install': True,
    'license': 'INCORE-1',
}
