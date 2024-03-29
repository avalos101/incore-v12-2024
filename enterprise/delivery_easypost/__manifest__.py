# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
{
    'name': "Easypost Shipping",
    'description': "Send your parcels through Easypost and track them online",
    'category': "Warehouse",
    'version': '1.0',
    'depends': ['delivery', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_carrier_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/carrier_type_views.xml',
    ]
}
