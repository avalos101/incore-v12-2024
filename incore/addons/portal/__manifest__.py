# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Customer Portal',
    'summary': 'Customer Portal',
    'sequence': '9000',
    'category': 'Hidden',
    'description': """
This module adds required base code for a fully integrated customer portal.
It contains the base controller class and base templates. Business addons
will add their specific templates and controllers to extend the customer
portal.

This module contains most code coming from incore v10 website_portal. Purpose
of this module is to allow the display of a customer portal without having
a dependency towards website edition and customization capabilities.""",
    'depends': ['http_routing', 'mail'],
    'data': [
        'data/portal_data.xml',
        'views/assets.xml',
        'views/portal_templates.xml',
        'wizard/portal_share_views.xml',
        'wizard/portal_wizard_views.xml',
    ],
    'qweb': [
        'static/src/xml/portal_chatter.xml',
        'static/src/xml/portal_signature.xml',
    ],
}