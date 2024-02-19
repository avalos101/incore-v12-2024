# -*- coding: utf-8 -*-
{
    'name': 'Dian - Emisión electrónica Colombiana',
    'description': "Addon para enviar documentos a Dian",
    'author': "inCore",
    'summary': "Emisión de documentos contables a Dian",
    'version': '0.1',
    "license": "OPL-1",
    'currency':'USD',
    'category': 'module_category_account_voucher',
    "images": ["images/banner.png"],
        # any module necessary for this one to work correctly
    'depends': ['base','account','delivery'],

    # always loaded
    'data': [
#                'security/ir.model.access.csv',
                'views/views.xml',
                'views/templates.xml',
                'views/template_invoice.xml',
                'views/edocs.xml'
            ],
    'qweb': [
                'static/src/xml/pos.xml',
                'static/src/xml/website.xml'
            ],
    #"external_dependencies": {"python" : ["pytesseract"]},
    'installable': True,
}
