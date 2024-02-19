# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
{
    'name': "bpost Shipping",
    'description': """
Send your shippings through bpost and track them online
=======================================================

Companies located in Belgium can take advantage of shipping with the
local Post company.

See: https://www.bpost.be/portal/goHome
    """,
    'category': 'Warehouse',
    'version': '1.0',
    'depends': ['delivery', 'mail'],
    'data': [
        'data/delivery_bpost_data.xml',
        'views/delivery_bpost_views.xml',
        'views/res_config_settings_views.xml',
        'views/bpost_request_templates.xml',
    ],
    'license': 'INCORE-1',
}
