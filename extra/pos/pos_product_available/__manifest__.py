# Copyright 2014-2018  <https://incore.co/team/yelizariev>
# Copyright 2017 Gabbasov Dinar <https://incore.co/team/GabbasovDinar>
# Copyright 2018  <https://incore.co/team/KolushovAlexandr>
# Copyright 2018 Ildar Nasyrov <https://incore.co/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": """Available quantity of products in POS""",
    "summary": """Adds available quantity at products in POS""",
    "category": "Point Of Sale",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version={INCORE_BRANCH}",
    "images": [],
    "version": "12.0.1.0.6",
    "application": False,

    "author": "inCore",
    "support": "hola@incore.co",
    "website": "https://apps.incore.co/apps/modules/12.0/pos_product_available/",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        'point_of_sale',
        'stock',
    ],
    "external_dependencies": {"python": [], "bin": []},
    'data': [
        'data.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,
}
