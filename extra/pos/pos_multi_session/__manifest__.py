# Copyright 2017-2018  <https://incore.co/team/yelizariev>
# Copyright 2017-2018  <https://incore.co/team/KolushovAlexandr>
# Copyright 2017 Ilmir Karamov <https://incore.co/team/ilmir-k>
# Copyright 2017-2018 Dinar Gabbasov <https://incore.co/team/GabbasovDinar>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Sync POS orders across multiple sessions""",
    "summary": """Use multiple POS for handling orders""",
    "category": "Point Of Sale",
    "live_test_url": 'http://apps.it-projects.info/shop/product/pos-multi-session?version=12.0',
    "images": ["images/pos-multi-session.png"],
    "version": "12.0.4.2.5",
    "application": False,

    "author": "inCore",
    "support": "hola@incore.co",
    "website": "https://apps.incore.co/apps/modules/12.0/pos_multi_session/",
    "license": "LGPL-3",
    "price": 360.00,
    "currency": "EUR",

    "depends": [
        "pos_multi_session_sync"
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "data/pos_multi_session_data.xml",
        "security/ir.model.access.csv",
        "views/pos_multi_session_views.xml",
        "multi_session_view.xml"
    ],
    "qweb": [
        "static/src/xml/pos_multi_session.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,

    "demo_title": "Sync POS orders across multiple sessions",
    "demo_addons": [
        "pos_disable_payment",
        "pos_multi_session_sync",
        "pos_multi_session_restaurant",
    ],
    "demo_addons_hidden": [
    ],
    "demo_url": "pos-multi-session",
    "demo_summary": "Use multiple POSes for handling orders",
    "demo_images": [
        "images/pos-multi-session.png",
    ]
}
