# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Uruguay - Accounts Reports',
    'version': '1.1',
    'author': 'Uruguay l10n Team & Guillem Barba',
    'category': 'Accounting',
    'website': 'https://launchpad.net/incore-uruguay',
    'description': """
        Accounting reports for Uruguay

""",
    'depends': [
        'l10n_uy', 'account_reports',
    ],
    'data': [
        'data/account_financial_html_report_data.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'INCORE-1',
}
