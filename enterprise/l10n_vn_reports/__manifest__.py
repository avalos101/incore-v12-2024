# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

# This module is Copyright (c) 2009-2013 General Solutions (https://gscom.vn) All Rights Reserved.

{
    "name": 'Vietnam - Accounting Reports',
    "version": '1.1',
    "author": 'General Solutions',
    'website': 'https://gscom.vn',
    'category': 'Accounting',
    "description": """
This is the module to manage the accounting reports for Vietnam in inCore.
=========================================================================

This module applies to companies based in Vietnamese Accounting Standard (VAS).

**Credits:** General Solutions.
""",
    "depends": ['l10n_vn', 'account_reports'],
    "data": [
        'data/account_financial_html_report_data.xml',
    ],
    "installable": True,
    "auto_install": True,
    'license': 'INCORE-1',
}
