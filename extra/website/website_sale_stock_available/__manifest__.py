# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Product Availability',
    'summary': 'Manage product inventory & availability',
    'description': 'Add a new option to not show the product variants '
    'if it is not available.',
    'category': 'Website',
    'author': 'inCore',
    'website': 'https://incore.co',
    "maintainers": ["mamcode"],
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'version': '12.0.1.0.0',
    'depends': [
        'website_sale_stock',
        'incore_customize',
    ],
    'data': [
        'views/product_template_views.xml',
        'views/website_sale_stock_available_templates.xml',
    ],
    'installable': True,
}
