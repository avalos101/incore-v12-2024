# Copyright 2017 Ilmir Karamov <https://incore.co/team/ilmir-k>
# Copyright 2017-2018 Dinar Gabbasov <https://incore.co/team/GabbasovDinar>
# Copyright 2018  <https://incore.co/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Sync restaurant orders""",
    "summary": """Staff get order details immediately after waiter taps on tablet""",
    "category": "Point of Sale",
    "live_test_url": 'http://apps.it-projects.info/shop/product/pos-multi-session?version=12.0',
    "images": ['images/s2.png'],
    "version": "12.0.3.2.6",
    "application": False,

    "author": "inCore",
    "support": "hola@incore.co",
    "website": "https://apps.incore.co/apps/modules/12.0/pos_multi_session_restaurant/",
    "license": "LGPL-3",
    "price": 30.00,
    "currency": "EUR",

    "depends": [
        "pos_restaurant_base",
        "pos_multi_session",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/views.xml",
    ],
    "qweb": [
    ],
    "demo": [
        "demo/demo.xml",
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": True,
    "installable": True,
}
