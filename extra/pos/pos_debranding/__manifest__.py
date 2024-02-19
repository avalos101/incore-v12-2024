{
    'name': "POS debranding",
    'version': '12.0.1.0.0',
    'author': 'inCore',
    'license': 'LGPL-3',
    'category': 'Debranding',
    "support": "hola@incore.co",
    'website': 'https://www.incore.co/apps/modules/12.0/pos_debranding/',
    'depends': ['point_of_sale'],
    # 'price': 30.00,
    # 'currency': 'EUR',
    'data': [
        'views.xml',
        'template.xml'
    ],
    'qweb': [
        'static/src/xml/pos_debranding.xml',
    ],
    'installable': True,
}
