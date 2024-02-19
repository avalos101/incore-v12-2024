# -*- coding: utf-8 -*-
##############################################################################
#
#    inCore Development SAC.
#    Copyright (C) 2016-TODAY inCore (<http://incore.co>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'inCore partner extra technical data',
    'summary': 'incore partner extra data',
    'description': """incore partner extra technical data.
                        Aniade una pestania de informacion tecnica sobre el cliente 
    """,
    'category': 'Others',
    'version': '1.0',
    'website': 'http://www.incore.co/',
    'author': 'incore',
    'depends': ['base'],
    'data': [
        'views/partner_views.xml',
        'views/server_views.xml',
    ],
    'qweb': [],
    'application': True,
}
