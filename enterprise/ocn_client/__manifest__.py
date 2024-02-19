# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'inCore Cloud Notification Client (OCN)',
    'version': '1.0',
    'category': 'Tool',
    'summary': 'Allow push notification to devices',
    'description': """
inCore Cloud Notifications (OCN)
===============================

This module enables push notifications to registered devices for direct messages,
chatter messages and channel.
    """,
    'depends': ['iap', 'mail'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/ocn_assets.xml'
    ],
    'installable': True,
    'auto_install': True
}
