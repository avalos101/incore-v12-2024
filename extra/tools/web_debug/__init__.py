# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2017-Present inCore.  (<https://incore.co/>)
#   See LICENSE URL <https://store.incore.co/license.html/> for full copyright and licensing details.
#################################################################################
def pre_init_check(cr):
    from incore.service import common
    from incore.exceptions import Warning
    version_info = common.exp_version()
    server_serie =version_info.get('server_serie')
    if server_serie!='12.0':raise Warning('Module support inCore series 12.0 found {}.'.format(server_serie))
    return True
