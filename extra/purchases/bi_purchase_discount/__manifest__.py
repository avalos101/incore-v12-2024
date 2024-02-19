# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.


{
    'name': 'Purchase Order Lines with Discounts',
    'version': '12.0.0.1',
    'category': 'purchase',
    'summary': 'This apps help to define a discount per line in the purchase orders.',
    'description': """
        In this module you can add discounts in purchase lines.
        You will get discount on purhcase reports.
        Discounts in Purchase order lines
""",
    'license':'OPL-1',
    'author': 'inCore',
    'depends': ['base','purchase'],
    'data': [
            'views/purchase.xml',
            'views/inherit_purchase_report.xml'
    ],
    'installable': True,
    'auto_install': False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
