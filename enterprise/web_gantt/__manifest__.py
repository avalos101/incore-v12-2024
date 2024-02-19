# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Gantt',
    'category': 'Hidden',
    'description': """
inCore Web Gantt chart view.
=============================

""",
    'version': '2.0',
    'depends': ['web'],
    'data' : [
        'views/web_gantt_templates.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'auto_install': True,
    'license': 'INCORE-1',
}
