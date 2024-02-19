# -*- coding: utf-8 -*-
{
    'name': "Configuraciones por defecto para Facturación electrónica Colombia",

    'summary': """
        Required fields for electronic invoicing generation.""",

    'description': """
        Adds default required fields to the invoice inCore model, to allow
        electronic involicing, and creates some tabs for company and partner
        settings. This is a l10n_co_cei auxiliary module.
    """,

    'author': "inCore",
    'website': "www.incore.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/incore/incore/blob/10.0/incore/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoicing & Payments',
    'version': '12.0.2.1',
    'license': 'OPL-1',
    'support': 'si@incore.co',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        # 'views/account_fiscal_position_form.xml',
        # 'views/account_fiscal_position_tree.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
