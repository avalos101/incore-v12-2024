# Copyright 2017 Dinar Gabbasov <https://incore.co/team/GabbasovDinar>
# Copyright 2018 Artem Losev
# Copyright 2018 Ilmir Karamov <https://incore.co/team/ilmir-k>
# Copyright 2018  <https://incore.co/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "POS Orders History",
    "summary": """See all paid orders from special menu in POS""",
    "category": "Point of Sale",
    "live_test_url": "http://apps.it-projects.info/shop/product/pos-orders-history?version=12.0",
    "images": ['images/pos_orders_history_main.png'],
    "version": "12.0.1.2.0",
    "application": False,

    "author": "IT-Projects LLC, Dinar Gabbasov",
    "support": "hola@incore.co",
    "website": "https://apps.incore.co/apps/modules/12.0/pos_orders_history/",
    "license": "LGPL-3",
    "price": 59.00,
    "currency": "EUR",

    "depends": [
        "base_automation",
        "pos_longpolling",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/pos_orders_history_view.xml",
        "views/pos_orders_history_template.xml",
        "data/base_action_rule.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "demo": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,

    "demo_title": "POS Orders History",
    "demo_addons": [
    ],
    "demo_addons_hidden": [
    ],
    "demo_url": "pos-orders-history",
    "demo_summary": "See all paid orders from special menu in POS",
    "demo_images": [
        "images/pos_orders_history_main.png",
    ]
}
