# Copyright 2014  <https://incore.co/team/yelizariev>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": """Discount for total amount of pos order""",
    "summary": """Simple way to apply discount for all order items""",
    "category": "Point of Sale",
    "images": [],
    "version": "12.0.1.0.0",
    "application": False,

    "author": "inCore",
    "support": "hola@incore.co",
    "website": "https://apps.incore.co/apps/modules/12.0/pos_discount_total/",
    "license": "LGPL-3",
    "price": 15.00,
    "currency": "EUR",

    "depends": [
        "point_of_sale",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "data.xml",
    ],
    "demo": [],
    "qweb": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,
}
