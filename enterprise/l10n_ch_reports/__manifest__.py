# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Switzerland - Accounting Reports',
    'version': '1.1',
    'category': 'Accounting',
    'description': """
        Accounting reports for Switzerland
    """,
    'depends': [
        'l10n_ch', 'account_reports'
    ],
    'data': [
        'data/account_tax_data.xml',
        'data/account_vat2011_data.xml',
        'data/account_financial_html_report_data.xml',
    ],
    'installable': True,
    'auto_install': True,
    'website': 'https://www.incore.co/page/accounting',
    'license': 'INCORE-1',
}
