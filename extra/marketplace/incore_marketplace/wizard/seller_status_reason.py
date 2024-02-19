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

class SellerStatusReasonWizard(models.TransientModel):
    _name = 'seller.status.reason.wizard'
    _description = "Seller Status Reason Wizard"

    @api.model
    def _get_seller(self):
        return self._context.get('active_id', False)

    seller_id = fields.Many2one("res.partner", string="Seller", default=_get_seller, domain=[("seller", "=", True)])
    reason = fields.Text(string="Reason", required="1")

    @api.multi
    def do_denied(self):
        self.ensure_one()
        if self.seller_id:
            self.seller_id.deny()
            self.seller_id.status_msg = self.reason
            reason_msg = "Deny Reason : " + self.reason
            self.seller_id.message_post(body=reason_msg)
