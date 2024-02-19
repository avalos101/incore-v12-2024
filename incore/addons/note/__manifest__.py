# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Notes',
    'version': '1.0',
    'category': 'Tools',
    'description': "",
    'website': 'https://www.incore.co/page/notes',
    'summary': 'Organize your work with memos',
    'sequence': 45,
    'depends': [
        'mail',
    ],
    'data': [
        'security/note_security.xml',
        'security/ir.model.access.csv',
        'data/mail_activity_data.xml',
        'data/note_data.xml',
        'data/res_users_data.xml',
        'views/note_views.xml',
        'views/note_templates.xml',
        'views/mail_activity_views.xml',
    ],
    'demo': [
        'data/note_demo.xml',
    ],
    'qweb': [
        'static/src/xml/systray.xml',
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}