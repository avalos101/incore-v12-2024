# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present inCore.  (<https://incore.co/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.incore.co/license.html/>
#
#################################################################################
from . import models

def pre_init_check(cr):
	from incore.service import common
	from incore.exceptions import Warning
	version_info = common.exp_version()
	server_serie =version_info.get('server_serie')
	if server_serie!='12.0':raise Warning('Module support inCore series 11.0 found {}.'.format(server_serie))
	return True
