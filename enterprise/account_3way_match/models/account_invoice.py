# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import api, fields, models
from incore.tools.float_utils import float_compare

# Available values for the release_to_pay field.
_release_to_pay_status_list = [('yes', 'Yes'), ('no', 'No'), ('exception', 'Exception')]

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    release_to_pay = fields.Selection(
        _release_to_pay_status_list,
        compute='_compute_release_to_pay',
        copy=False,
        store=True,
        string='Should be paid',
        help="This field can take the following values :\n"
             "  * Yes: you should pay the bill, you have received the products\n"
             "  * No, you should not pay the bill, you have not received the products\n"
             "  * Exception, there is a difference between received and billed quantities\n"
             "This status is defined automatically, but you can force it by ticking the 'Force Status' checkbox.")
    release_to_pay_manual = fields.Selection(
        _release_to_pay_status_list,
        string='Should be paid Manual',
        help="  * Yes: you should pay the bill, you have received the products\n"
             "  * No, you should not pay the bill, you have not received the products\n"
             "  * Exception, there is a difference between received and billed quantities.")
    force_release_to_pay = fields.Boolean(
        string="Force status",
        help="Indicates whether the 'Can be paid' status is defined automatically or manually.")

    @api.depends('invoice_line_ids.can_be_paid', 'release_to_pay_manual', 'force_release_to_pay')
    def _compute_release_to_pay(self):
        for invoice in self:
            if invoice.force_release_to_pay and invoice.release_to_pay_manual:
                #we must use the manual value contained in release_to_pay_manual
                invoice.release_to_pay = invoice.release_to_pay_manual
            else:
                #otherwise we must compute the field
                result = None
                for invoice_line in invoice.invoice_line_ids:
                    line_status = invoice_line.can_be_paid
                    if line_status == 'exception':
                        #If one line is in exception, the entire bill is
                        result = 'exception'
                        break
                    elif not result:
                        result = line_status
                    elif line_status != result:
                        result = 'exception'
                        break
                    #The last two elif conditions model the fact that a
                    #bill will be in exception if its lines have different status.
                    #Otherwise, its status will be the one all its lines share.

                #'result' can be None if the bill was entirely empty.
                invoice.release_to_pay = result or 'no'


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.depends('purchase_line_id.qty_received', 'purchase_line_id.qty_invoiced', 'purchase_line_id.product_qty')
    def _can_be_paid(self):
        """ Computes the 'release to pay' status of an invoice line, depending on
        the invoicing policy of the product linked to it, by calling the dedicated
        subfunctions. This function also ensures the line is linked to a purchase
        order (otherwise, can_be_paid will be set as 'exception'), and the price
        between this order and the invoice did not change (otherwise, again,
        the line is put in exception).
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for invoice_line in self:
            po_line = invoice_line.purchase_line_id
            if po_line:
                invoiced_qty = po_line.qty_invoiced
                received_qty = po_line.qty_received
                ordered_qty = po_line.product_qty

                # A price difference between the original order and the invoice results in an exception
                invoice_currency = invoice_line.currency_id
                order_currency = po_line.currency_id
                invoice_converted_price = invoice_currency._convert(
                    invoice_line.price_unit, order_currency, invoice_line.company_id, fields.Date.today())
                if order_currency.compare_amounts(po_line.price_unit, invoice_converted_price) != 0:
                    invoice_line.can_be_paid = 'exception'
                    continue

                if po_line.product_id.purchase_method == 'purchase': # 'on ordered quantities'
                    invoice_line._can_be_paid_ordered_qty(invoiced_qty, received_qty, ordered_qty, precision)
                else: # 'on received quantities'
                    invoice_line._can_be_paid_received_qty(invoiced_qty, received_qty, ordered_qty, precision)

            else: # Serves as default if the line is not linked to any Purchase.
                invoice_line.can_be_paid = 'exception'

    def _can_be_paid_ordered_qty(self, invoiced_qty, received_qty, ordered_qty, precision):
        """
        Gives the release_to_pay status of an invoice line for 'on ordered
        quantity' billing policy, if this line's invoice is related to a purchase order.

        This function sets can_be_paid field to one of the following:
        'yes': the content of the line has been ordered and can be invoiced
        'no' : the content of the line hasn't been ordered at all, and cannot be invoiced
        'exception' : only part of the invoice has been ordered
        """
        if float_compare(invoiced_qty - self.quantity, ordered_qty, precision_digits=precision) >= 0:
            self.can_be_paid = 'no'
        elif float_compare(invoiced_qty, ordered_qty, precision_digits=precision) <= 0:
            self.can_be_paid = 'yes'
        else:
            self.can_be_paid = 'exception'


    def _can_be_paid_received_qty(self, invoiced_qty, received_qty, ordered_qty, precision):
        """
        Gives the release_to_pay status of an invoice line for 'on received
        quantity' billing policy, if this line's invoice is related to a purchase order.

        This function sets can_be_paid field to one of the following:
        'yes': the content of the line has been received and can be invoiced
        'no' : the content of the line hasn't been received at all, and cannot be invoiced
        'exception' : ordered and received quantities differ
        """
        if float_compare(invoiced_qty, received_qty, precision_digits=precision) <= 0:
            self.can_be_paid = 'yes'
        elif received_qty == 0 and float_compare(invoiced_qty, ordered_qty, precision_digits=precision) <= 0: # "and" part to ensure a too high billed quantity results in an exception:
            self.can_be_paid = 'no'
        else:
            self.can_be_paid = 'exception'

    can_be_paid = fields.Selection(
        _release_to_pay_status_list,
        compute='_can_be_paid',
        copy=False,
        store=True,
        string='Release to Pay')
