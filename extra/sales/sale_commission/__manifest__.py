# Copyright 2014-2018 Tecnativa - Pedro M. Baeza
{
    'name': 'Sales commissions',
    'version': '12.0.1.1.0',
    'author': 'inCore',
    'category': 'Sales Management',
    'depends': [
        'account',
        'product',
        'sale_management',
    ],
    'development_status': 'Mature',
    'maintainers': [
        'pedrobaeza',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_commission_view.xml',
        'views/sale_commission_mixin_views.xml',
        'views/product_template_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/account_invoice_view.xml',
        'views/sale_commission_settlement_view.xml',
        'views/sale_commission_settlement_report.xml',
        'views/report_settlement_templates.xml',
        'report/sale_commission_analysis_report_view.xml',
        'wizard/wizard_settle.xml',
        'wizard/wizard_invoice.xml',
    ],
    'demo': [
        'demo/sale_agent_demo.xml',
    ],
    'installable': True,
}
