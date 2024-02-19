# -*- coding: utf-8 -*-

{
    'name': 'ADDI Payment Acquirer',
    'category': 'Payment / Colombia',
    'author': '',
    'summary': 'Payment Acquirer: Colombian ADDI Payment Acquirer',
    'website': '',
    'version': "0.1",
    'description': """Colombian ADDI Payment Acquirer""",
    'depends': [
            'payment',
            'website_sale',
            'l10n_co',
    ],
    'data': [
        'data/payment_icon_data.xml',
        'views/res_partner.xml',
        'views/addi_template.xml',
        'views/payment_acquirer.xml',
        'views/website_checout.xml',
        'data/addi.xml',
    ],
    'installable': True,
    'application': True,
}
