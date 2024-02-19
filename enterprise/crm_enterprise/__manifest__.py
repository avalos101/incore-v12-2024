# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': "CRM enterprise",
    'version': "1.0",
    'category': "Sales",
    'summary': "Advanced features for CRM",
    'description': """
Contains advanced features for CRM such as new views
    """,
    'depends': ['crm', 'web_dashboard', 'web_cohort'],
    'data': [
        'views/crm_lead_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}