# -*- encoding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Thailand - Accounting Reports',
    'version': '1.1',
    'description': """
Accounting reports for Thailand
================================
    """,
    'author': ['Almacom'],
    'website': 'http://almacom.co.th/',
    'category': 'Accounting',
    'depends': ['l10n_th', 'account_reports'],
    'data': [
        'data/account_financial_html_report_data.xml',
    ],
    'demo': [],
    'auto_install': True,
    'installable': True,
    'license': 'INCORE-1',
}
