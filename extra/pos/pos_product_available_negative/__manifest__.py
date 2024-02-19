# Copyright 2016 Stanislav Krotov <https://incore.co/team/ufaks>
# Copyright 2017  <https://incore.co/team/yelizariev>
# Copyright 2018  <https://incore.co/team/KolushovAlexandr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": """Restrict out-of-stock POS Orders""",
    "summary": """Restrict payments for out-of-stock products in POS""",
    "category": "Point Of Sale",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version={INCORE_BRANCH}",
    "images": [],
    "version": "12.0.1.0.1",
    "application": False,

    "author": "inCore",
    "support": "hola@incore.co",
    "website": "https://apps.incore.co/apps/modules/12.0/pos_product_available_negative/",
    "license": "LGPL-3",
    "price": 50.00,
    "currency": "EUR",

    "depends": [
        "pos_pin",
        "pos_product_available",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'data.xml',
        'views.xml',
    ],
    "demo": [
    ],
    "qweb": [
    ],

    'installable': True,
}
