# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Checklist of products in inventory',
    'summary': 'Allow check products before validate the inventory',
    'category': 'Stock',
    'author': 'inCore',
    "maintainers": ["mamcode"],
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'version': '12.0.1.0.0',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_inventory_views.xml',
    ],
    'installable': True,
}
