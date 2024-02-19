# -*- coding: utf-8 -*-


from incore import api, models, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_cancel(self):
        for purchase in self:
            for invoice in purchase.invoice_ids :
                if invoice.state != 'cancel':
                    invoice.action_invoice_cancel()
            for picking in purchase.picking_ids:
                if picking.state != 'cancel':
                    picking.picking_cancel()
        self.write({'state': 'cancel'})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
