# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'PoS Order Margin',
    'summary': 'Margin on PoS Order',
    'version': '12.0.2.0.1',
    'category': 'Point Of Sale',
    'author': "GRAP,"
              "incore Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    'website': 'https://github.com/OCA/pos',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'sale_margin',
    ],
    'data': [
        'views/templates.xml',
        'views/view_pos_config.xml',
        'views/view_pos_order.xml',
    ],
    'qweb': [
        'static/src/xml/pos_margin.xml',
    ],
    'installable': True,
}
