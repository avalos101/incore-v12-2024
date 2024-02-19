# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Incore Ecommerce Checkout Custom',
    'summary': 'Checkout form view customized.',
    'description': 'Checkout form view customized.',
    'category': 'Website',
    'author': 'inCore',
    'website': 'https://incore.co',
    "maintainers": ["mamcode"],
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'version': '12.0.1.0.0',
    'depends': [
        'website_sale',
        'l10n_co_res_partner',
    ],
    'data': [
        'data/ir_model_fields.xml',
        'views/templates.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
