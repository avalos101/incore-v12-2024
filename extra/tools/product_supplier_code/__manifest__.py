# -*- coding: utf-8 -*-


{
    'name': 'Código de proveedor en el producto',
    'summary': """
    Codigo del proveedor en el producto
    """,
    "version": '0.0.2',
    'category': 'Product',
    'author': 'Gustavo H.',
    'license': 'AGPL-3',
    'sequence': 3,
    'installable': True,
    'auto_install': False,
    'application': True,
    'description': """
        Codigo del proveedo en plantilla del producto
    """,
    'depends': [
        'product',
                ],
    'data': [
        'views/product_template_views.xml',
        'views/product_product_views.xml',
    ],
    'demo': [
    ],
}
