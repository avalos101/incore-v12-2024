# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.


{
    'name': 'Appointments',
    'version': '1.0',
    'category': 'Website',
    'sequence': 131,
    'summary': 'Schedule appointments with clients',
    'website': 'https://www.incore.co/page/appointments',
    'description': """
Allow clients to Schedule Appointments through your Website
-------------------------------------------------------------

""",
    'depends': ['calendar_sms', 'website_enterprise', 'hr'],
    'data': [
        'data/website_calendar_data.xml',
        'views/calendar_views.xml',
        'views/calendar_appointment_views.xml',
        'views/website_calendar_templates.xml',
        'security/website_calendar_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'data/website_calendar_demo.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'INCORE-1',
}
