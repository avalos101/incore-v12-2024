# Copyright 2017  <https://incore.co/team/yelizariev>
# Copyright 2017  <https://incore.co/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Sync Server for POS orders""",
    "summary": """Sync orders via main or separate (e.g. local) server""",
    "category": "Point of Sale",
    "live_test_url": 'http://apps.it-projects.info/shop/product/pos-multi-session?version=12.0',
    "images": [],
    "version": "12.0.1.0.3",
    "application": False,

    "author": "IT-Projects LLC, ",
    "support": "hola@incore.co",
    "website": "https://apps.incore.co/apps/modules/12.0/pos_multi_session_sync/",
    "license": "LGPL-3",
    "price": 60.00,
    "currency": "EUR",

    "depends": [
        "pos_longpolling",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv"
    ],
    "qweb": [
    ],
    "demo": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
