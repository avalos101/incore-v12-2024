# -*- coding: utf-8 -*-
#################################################################################
# Author      : inCore.  (<https://incore.co/>)
# Copyright(c): 2015-Present inCore. 
# License URL : https://store.incore.co/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.incore.co/license.html/>
#################################################################################

from . import wizard
from . import models
from . import controllers

def pre_init_check(cr):
    from incore.service import common
    from incore.exceptions import Warning
    version_info = common.exp_version()
    server_serie =version_info.get('server_serie')
    if server_serie!='12.0':raise Warning('Module support inCore series 12.0 found {}.'.format(server_serie))
    return True