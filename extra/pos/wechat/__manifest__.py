# Copyright 2018  <https://incore.co/team/yelizariev>
# Copyright 2018 Dinar Gabbasov <https://incore.co/team/GabbasovDinar>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """WeChat API""",
    "summary": """Technical module to integrate inCore with WeChat""",
    "category": "Hidden",
    # "live_test_url": "",
    "images": [],
    "version": "12.0.1.0.1",
    "application": False,

    "author": "inCore",
    "support": "hola@incore.co",
    "website": "https://apps.incore.co/apps/modules/12.0/wechat/",
    "license": "LGPL-3",
    "price": 150.00,
    "currency": "EUR",

    "depends": [
        'product',
        'account',
        'qr_payments',
    ],
    "external_dependencies": {"python": [
        'wechatpy',
    ], "bin": []},
    "data": [
        "views/account_menuitem.xml",
        "views/wechat_micropay_views.xml",
        "views/wechat_order_views.xml",
        "views/wechat_refund_views.xml",
        "views/account_journal_views.xml",
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
    ],
    "qweb": [],

    "auto_install": False,
    "installable": True,
}
