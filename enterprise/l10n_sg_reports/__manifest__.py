# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Singapore - Accounting Reports',
    'version': '1.1',
    'author': 'Tech Receptives',
    'website': 'http://www.techreceptives.com',
    'category': 'Accounting',
    'description': """
Accounting reports for Singapore
================================
This module allow to generate the GST Return (F5) and the IRAS Audit File.
 - To generate the GST Return, go to Accounting -> Reporting -> GST Return
 - To generate the IRAS Audit File, go to Accounting -> Reporting -> IRAS Audit File
    """,
    'depends': [
        'l10n_sg', 'account_reports'
    ],
    'data': [
        'data/account_iras_audit_file_data.xml',
        'data/account_gst_returns_data.xml',
        'views/iaf_template.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'INCORE-1',
}
