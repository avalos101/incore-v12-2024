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

from incore import models, fields, api, _


class seller_payment_method(models.Model):
    _name = "seller.payment.method"
    _description = "Seller Payment Method"

    name = fields.Char(string="Payment Method", required=True,  translate=True)
