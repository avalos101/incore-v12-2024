# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Incore Signup Custom',
    'summary': 'Signup form view customized.',
    'description': 'Signup form view customized.',
    'category': 'Website',
    'author': 'inCore',
    'website': 'https://incore.co',
    "maintainers": ["mamcode"],
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'version': '12.0.1.0.0',
    'depends': [
        'web',
        'l10n_co_res_partner',
        'incore_jl_website_sale_checkout',
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
}
