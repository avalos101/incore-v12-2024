# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sell Helpdesk Timesheet',
    'category': 'Hidden',
    'summary': 'Project, Helpdesk, Timesheet and Sale Orders',
    'depends': ['helpdesk_timesheet', 'sale_timesheet'],
    'description': """
        Bill timesheets logged on helpdesk tickets.
    """,
    'auto_install': True,
    'data': [
        'views/helpdesk_views.xml',
    ],
    'demo': [
        'data/helpdesk_sale_timesheet_demo.xml',
    ],
}
