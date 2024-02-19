# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from incore import models, fields, api

class PosConfig(models.Model):
    _inherit="pos.config"

    open_pricelist_popup = fields.Char('Shortcut Key')
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: