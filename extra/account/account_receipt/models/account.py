# -*- coding: utf-8 -*-

from incore import api, fields, models, tools, _


class AccountPrintReceipt(models.TransientModel):
    _name = 'account.print.receipt'

    name = fields.Char("Test")


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    multi_due = fields.Boolean(
        string='Multiple date due',
        compute='_compute_multi_due'
    )
    multi_date_due = fields.Char(
        string='Due Dates',
        compute='_compute_multi_date_due'
    )

    @api.depends('payment_term_id')
    def _compute_multi_due(self):
        for invoice in self:
            invoice.multi_due = len(invoice.payment_term_id.line_ids) > 1

    @api.depends('move_id', 'payment_term_id', 'date_invoice')
    def _compute_multi_date_due(self):
        lang = self.env.context.get('lang') or 'en_US'
        date_format = self.env['res.lang']._lang_get(lang).date_format
        for invoice in self:
            invoice.multi_date_due = ' '.join(
                fields.Date.from_string(due[0]).strftime(date_format)
                for due in invoice.get_multi_due_list())

    def get_multi_due_list(self):
        self.ensure_one()
        due_list = []
        if self.move_id:
            if self.type in ['in_invoice', 'out_refund']:
                due_move_line_ids = self.move_id.line_ids.filtered(
                    lambda ml: ml.account_id.internal_type == 'payable'
                )
            else:
                due_move_line_ids = self.move_id.line_ids.filtered(
                    lambda ml: ml.account_id.internal_type == 'receivable'
                )
            if self.currency_id != self.company_id.currency_id:
                due_list = [
                    (ml.date_maturity, ml.amount_currency)
                    for ml in due_move_line_ids]
            else:
                due_list = [
                    (ml.date_maturity, ml.balance)
                    for ml in due_move_line_ids]
        elif self.payment_term_id:
            date_invoice = (
                self.date_invoice or fields.Date.context_today(self))
            due_list = self.payment_term_id.with_context(
                currency_id=self.company_id.currency_id.id).compute(
                value=self.amount_total, date_ref=date_invoice)[0]
        due_list.sort()
        return due_list

    @api.multi
    def print_new_receipt(self):
        logo = (self.company_id.logo).decode()
        partner_vat = str(self.partner_id.xidentification or self.partner_id.vat or '')  
        website = self.company_id.website.replace('http://','').replace('https://','')
        header = self.journal_id.report_header or ''

        ticket = """
            <div class="pos-sale-ticket">
                <div class="text-center" style="text-align: center !important;">
                    <img src="data:image/png;base64,"""+logo+"""" alt="Logo" style="max-height:2cm; max-width:100%;"/>
                    <br/>
                    <div><strong><h2 class="comp">"""+self.company_id.name+"""</h2></strong></div>
                    <span>"""+website+"""</span><br/>
                    <div><span>"""+self.company_id.vat +" Tel: "+self.company_id.phone+"""</span></div>
                </div>
                <hr/>
                <div style="text-align: center !important;">
                    """+header+"""
                </div>
                <hr/>
                <table>
                    <colgroup>
                        <col width='25%' />
                        <col width='75%' />
                    </colgroup>
                    <tr><td colspan="2">Factura de venta: """ + self.number + """</td></tr>
                    <tr><td>Fecha:</td><td>""" + str(self.date_invoice) + """</td></tr>
                    <tr><td>Vendedor:</td><td>""" + self.x_studio_vendedor.name + """</td></tr>
                    <tr><td>Cajero:</td><td>""" + self.user_id.partner_id.name+ """</td></tr>
                    <tr><td>Cliente:</td><td>"""+ self.partner_id.name +"""</td></tr>
                    <tr><td>Cedula:</td><td>""" + partner_vat + """</td></tr>
                </table>
                <hr/>
                <table class='receipt-orderlines'>
                    <colgroup>
                        <col width='65%' />
                        <col width='35%' />
                    </colgroup>
                    <tr style="border-bottom:1px solid #dddddd;">
                        <th class="pos-left-align" width="70%"><h3 class="descrip">Descripción<br/>Cant./Precio Unit.</h3></th>
                        <th class="pos-right-align" width="30%"><h3 class="descrip">Importe</h3></th>
                    </tr>"""
        detalle = ""
        for line in self.invoice_line_ids:
            line_subtotal = "%s%s" %(self.currency_id.symbol, str('{:,.0f}'.format(line.price_subtotal))) 
            descripcion = line.name
            if line.product_id:
                default_code = "[%s]" %line.product_id.default_code
                # if default_code in line.name:
                #     descripcion = line.name.replace(line.product_id.default_code, line.product_id.barcode or '')
                # else:
                #     if line.product_id.barcode:
                #         descripcion = "[%s] %s" %(line.product_id.barcode, line.name)
                descripcion = "[%s] %s" %(line.product_id.barcode or '', line.product_id.product_tmpl_id.name)

            detalle += """ <tr>
                        <td class="pos-left-align">
                            """+descripcion+"""<br/>
                            <t t-if="orderline.get_discount() > 0">
                                <div class="pos-disc-font">
                                    Con un """+str(line.discount)+"""% de descuento
                                </div>
                            </t>
                            <left>
                                <line indent="1">
                                    """+ str(line.quantity)+" X "+str('{:,.0f}'.format(line.price_unit))+"""
                                </line>
                            </left>
                        </td>
                        <td class="pos-right-align">
                            """+line_subtotal+"""
                        </td>
                    </tr>"""
        totales = """</table>
            <hr/>
            <table class='receipt-total'>
                <tr>
                    <td>BASE:</td>
                    <td class="pos-right-align">
                        """+self.currency_id.symbol +" "+ str('{:,.0f}'.format(self.amount_untaxed))+"""
                    </td>
                </tr>
                <tr>
                    <td>IVA:</td>
                    <td class="pos-right-align">
                        """+self.currency_id.symbol +" "+ str('{:,.0f}'.format(self.amount_tax)) +"""
                    </td>
                </tr>
                <tr class="emph">
                    <td>TOTAL:</td>
                    <td class="pos-right-align">
                        """+self.currency_id.symbol +" "+ str('{:,.0f}'.format(self.amount_total)) +"""
                    </td>
                </tr>
                <tr class="emph">
                    <td>Cuota Inicial:</td>
                    <td class="pos-right-align">
                        """+self.currency_id.symbol +" "+ str('{:,.0f}'.format(self.inicial_estimada)) +"""
                    </td>
                </tr>
                <tr class="emph">
                    <td>Importe Adeudado:</td>
                    <td class="pos-right-align">
                        """+self.currency_id.symbol +" "+ str('{:,.0f}'.format(self.residual)) +"""
                    </td>
                </tr>
            </table>
            <hr/>
            <div class="pos-center-align" style="text-align: center;"></br>
                """+str(self.cronograma2)+"""
            </div>
            """
        cronograma = ""
        # cronograma = self.cronograma
        # cronograma = """
        #                     <table class='receipt-paymentlines'>
        #                         <tr>
        #                             <td class="text-center" colspan="5">Cronograma</td>
        #                         </tr>"""
        # for in self:
        #         <t t-foreach="paymentlines" t-as="line">
        #           <tr>
        #               <td>
        #                   <t t-esc="line.name"/>
        #               </td>
        #               <td class="pos-right-align">
        #                   <t t-esc="widget.format_currency(line.get_amount())"/>
        #               </td>
        #           </tr>
        #         </t>
        #     </table>
        # </div> """

        # footer = "Estimado cliente, los artículos de joyería son delicados y susceptibles a golpes, jalones y químicos. Úselos con cuidado ya que la garantía solo cubre la autenticidad de los materiales. Los artículos de plata reaccionan con ciertos elementos en el ambiente lo cual produce pérdida de brillo y oxidación, use nuestro liquido brillador para llevarlos a su brillo original. No se hacen devoluciones de dinero. Se aceptan cambios de mercancía sin usar y en perfectas condiciones presentando la factura original y todos los empaques,  manuales y demás entregados hasta 30 días después de la compra; no aplica  para órdenes especiales o mercancía en promoción. Leído y recibido en perfecto estado por:"
        # if self.journal_id.footer:
        footer = self.journal_id.report_footer or ''
        slogan = """
            <hr/>
            <center>
            <img style="width:300px;height:50px;" alt="Código de barras" src="/report/barcode/?type=Code128&amp;value="""+self.number+"""&amp;width=600&amp;height=100">
            <br/>
            """+self.number+"""
            </center>
            <br/>
            <div style="text-align: center !important;">
                """+footer+"""
            </div>
            <br/>
            <center>
            ___________________________
            </center>
            <br/>
            <br/>
            <div style="text-align: center !important;">MUCHAS GRACIAS POR SU VISITA!</div>
            """
        
        text_val = ticket + detalle + totales + cronograma + slogan
        res = {"name":text_val,}
        wizard_id = self.env['account.print.receipt'].create(res)
        view_id = self.env.ref('account_receipt.account_print_receipt_form').id

        context = self._context.copy()
        return {
            'name':'Print Receipt',
            'view_type':'form',
            'view_mode':'tree',
            'views' : [(view_id,'form')],
            'res_model':'account.print.receipt',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':wizard_id.id,
            'target':'new',
            'context':context,

        }