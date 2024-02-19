# -*- coding: utf-8 -*-
{
    'name': "Campos extra en contratos de empleado",

    'summary': """Añade campos extra al modelo del contrato""",

    'description': """
        Añadde campos relacionados a las afiliaciones de un empleado tales como:
            -Salud (EPS)
            -Pensiones (AFP)
            -Cesantiaas (AFC)
            -Caja compensacion
            -Riesgos laborales (ARL)
    """,

    'author': "León Avalos",
    'website': "http://www.leon-avalos.com",
    'category': 'HHRRR',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/templates.xml',
        'views/views.xml',
    ],
}