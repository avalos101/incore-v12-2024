# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "POS Backend Communication",
    "summary": "Communicate with incore's backend from POS.",
    "version": "1.0.0",
    "category": "Point of Sale",
    "website": "http://www.akretion.com",
    'author': 'Akretion, inCore ',
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "depends": [
        "point_of_sale",
    ],
    "data": [
        'views/assets.xml',
    ],
}
