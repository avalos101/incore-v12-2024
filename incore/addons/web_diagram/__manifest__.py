# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'inCore Web Diagram',
    'category': 'Hidden',
    'description': """
Incore Web Diagram view.
=========================

""",
    'version': '2.0',
    'depends': ['web'],
    'data': [
        'views/web_diagram_templates.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'auto_install': True,
}
