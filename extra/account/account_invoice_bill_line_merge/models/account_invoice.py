# -*- coding: utf-8 -*-
from incore import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def merge_invoice_line(self):
        invoice_id = self.env['account.invoice.line'].read_group(
            [('invoice_id', '=', self.id)], ['product_id', 'quantity'], ['product_id'])
        for invoice in invoice_id:
            line_ids = self.env['account.invoice.line'].search(
                [('invoice_id', '=', self.id), ('product_id', '=', invoice['product_id'][0])])
            main_line = line_ids[0]
            line_ids[1:].unlink()
            main_line.quantity = invoice['quantity']

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        if res.type == 'out_invoice' and self.env.user.company_id.auto_merge_invoice_line:
            res.merge_invoice_line()
        if res.type == 'in_invoice' and self.env.user.company_id.auto_merge_bill_line:
            res.merge_invoice_line()
        return res

    @api.multi
    def write(self, vals):
        res = super(AccountInvoice, self).write(vals)
        if 'invoice_line_ids' in vals and self.type == 'out_invoice' and self.env.user.company_id.auto_merge_invoice_line:
            self.merge_invoice_line()
        if 'invoice_line_ids' in vals and self.type == 'in_invoice' and self.env.user.company_id.auto_merge_bill_line:
            self.merge_invoice_line()
        return res
