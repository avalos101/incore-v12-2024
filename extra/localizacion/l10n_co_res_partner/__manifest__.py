# -*- coding: utf-8 -*-

{
    'name': 'Localizacion de Terceros para Colombia',
    'category': 'Localization',
    'version': '12.0',
    'author': 'inCore',
    'license': 'AGPL-3',
    'website': 'www.incore.co',
    'summary': 'Colombia Terceros: Extended Partner / '
               'Contact Module - inCore 12.0',
    'depends': [
    'base',
    'l10n_co',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/l10n_co_res_partner.xml',
        'data/l10n_cities_co_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
