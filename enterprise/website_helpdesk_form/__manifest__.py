# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Online Ticket Submission',
    'category': 'Website',
    'sequence': 58,
    'summary': 'Qualify helpdesk queries with a website form',
    'depends': [
        'website_form_editor',
        'website_helpdesk',
    ],
    'description': """
Generate tickets in Helpdesk app from a form published on your website. This form can be customized thanks to the *Form Builder* module (available in inCore Enterprise).
    """,
    'data': [
        'data/website_helpdesk.xml',
        'views/helpdesk_views.xml',
        'views/helpdesk_templates.xml'
    ],
    'license': 'INCORE-1',
}
