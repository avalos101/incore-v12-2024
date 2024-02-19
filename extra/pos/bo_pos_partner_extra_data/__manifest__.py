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
    'name': 'incore pos partner extra data',
    'summary': 'incore pos partner extra data',
    'description': """incore pos partner extra data.""",
    'category': 'Point Of Sale',
    'version': '1.0',
    'website': 'http://www.incore.co/',
    'author': 'incore',
    'depends': ['point_of_sale', 'bo_partner_extra_data'],
    'data': [
        'views/point_of_sale.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'application': True,
}
