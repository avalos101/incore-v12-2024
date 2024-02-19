# -*- coding: utf-8 -*-


from incore import api, models, _

class SalesOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_cancel(self):
        for sale_order in self:
#            for invoice in sale_order.invoice_ids :
#                if invoice.state != 'cancel':
#                    invoice.action_invoice_cancel()
            for picking in sale_order.picking_ids:
                if picking.state != 'cancel':
                    picking.picking_cancel()
            sale_order.write({'state': 'cancel'})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
