# -*- coding: utf-8 -*-
{
    'name': 'Pos Combo Item Selection',
    'summary': "Show Combo Items in POS on selecting Combo item before add in cart",
    'description': 'Show Combo Items in POS on selecting Combo item',

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    "support": "ipredictitsolutions@gmail.com",

    'category': 'Point of Sale',
    'version': '12.0.0.1.0',
    'depends': ['pos_combo_product'],

    'data': [
        'views/pos_pack_template_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos_view.xml'
    ],

    'license': "OPL-1",
    'price': 5,
    'currency': "EUR",

    'installable': True,

    'images': ['static/description/main.png'],
}
