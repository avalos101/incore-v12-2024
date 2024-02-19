# -*- coding: utf-8 -*-

from incore import api, fields, models, tools, _


class PaymentPrintReceipt(models.TransientModel):
    _name = 'payment.print.receipt'
    name = fields.Char("Test")


class PaymentInvoice(models.Model):
    _inherit = "account.payment"

###############################################################################


    @api.multi
    def print_new_receipt(self):
        view_id = self.env.ref('payment_receipt.payment_print_receipt_form').id

        text_val = """
                <div class="pos-sale-ticket">
                    <div class="div-center" style="text-align: center;">
                        <br/>
                        <strong>
                        <h2>"""+str(self.company_id.name)+"""</h2>
                        """+str(self.company_id.vat)+"""<br/>
                        """+str(self.company_id.street)+"""</br>
                        """+str(self.company_id.phone)+"""</br>
                        </strong>
                        <br/>"""+str(self.company_id.company_registry)+"""

                    </div>

                    </br>
                    <strong>Comprobante de pago N:</strong> """+str(self.name)+"""</br>
                    <strong>Fecha:</strong> """+str(self.payment_date)+"""</br>
                    <strong>Recibio:</strong> """+str(self.create_uid.name)+"""</br>

                    <strong>Cliente:</strong> """+str(self.partner_id.name)+"""<br/>
                    <strong>Cedula:</strong>"""+str(self.partner_id.xidentification)+"""<br/>
                    <strong>Telefono:</strong>"""+str(self.partner_id.phone)+"""<br/>
                    <br/>
                    <div class="pos-center-align" style="text-align: center;">
                    </br>
                    Detalles del pago
                        _______________________________________________
                        </br>
                        <strong>Valor Pagado: $</strong>
                        """+str(self.amount)+"""</br>
                        <strong>Metodo de pago:</strong>
                        """+str(self.journal_id.name)+"""
                        </br>
                    </div>


            		<table class="receipt-orderlines">
		                <colgroup>
		                    <col width="50%"/>
		                    <col width="25%"/>
		                    <col width="25%"/>
		                </colgroup>
                	<tbody>
            <div class="pos-center-align" style="text-align: center;">
            </br>

            Firma:
            </br>
            </br>
            </br>
                _______________________________________________

                """+str(self.company_id.website)+"""
                </br>
            </div>
            </div>

            """
        res = {"name":text_val,}
        wizard_id = self.env['payment.print.receipt'].create(res)

        context = self._context.copy()
        return {
            'name':'Print Receipt',
            'view_type':'form',
            'view_mode':'tree',
            'views' : [(view_id,'form')],
            'res_model':'payment.print.receipt',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':wizard_id.id,
            'target':'new',
            'context':context,

        }
