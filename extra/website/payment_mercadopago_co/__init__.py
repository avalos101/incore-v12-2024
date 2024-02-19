# -*- coding: utf-8 -*-
##############################################################################
#
#    inCore, Open Source Management Solution
#    Copyright (C) 2013-Today inCore SA (<http://www.incore.com>).
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

from . import models
from . import controllers
from incore.addons.payment.models.payment_acquirer import create_missing_journal_for_acquirers
