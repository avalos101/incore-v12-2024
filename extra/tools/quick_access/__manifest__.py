{
    'name': 'Quick Access',
    'version': '12.0.0.0.0',
    'sequence': 14,
    'summary': 'Quick Access to any menu in your installed module',
    'author': 'Mostafa Mahmoud Abbas',
    "price": 9.00,
    'currency': 'EUR',
    'license': 'OPL-1',
    'images': [
        'images/main_screenshot.png',
    ],
    'depends': [
        'base','web'
    ],
    'data': [
        'views/quick_access_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
