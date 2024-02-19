# -*- coding: utf-8 -*-


{
    'name': 'Whatsapp Redirect integration',
    'summary': 'Redirect web browser of whatsapp',
    'description': 'Send Message to partner via Whatsapp web',
    'version': '12.0',
    'author': "inCore",
    'category': 'Extra Tools',
    'depends': ['base'],
    'data': [
        'views/res_partner_view.xml',
    ],

    'images': ['static/description/banner.png'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    'license': 'AGPL-3',
}
