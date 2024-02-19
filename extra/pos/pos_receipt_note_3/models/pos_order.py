# -*- coding: utf-8 -*-

from incore import api, fields, models, tools, _


class AccountPrintReceipt(models.TransientModel):
    _name = 'pos.print.receipt'

    name = fields.Char("POS test")


class PorOrder(models.Model):
    _inherit = "pos.order"

    @api.multi
    def get_order_values(self):
        val = {
            'order_name': self.name
        }
        return val

    @api.multi
    def print_new_receipt(self):
        values = []
        if self.company_id.logo:
            values.append((self.company_id.logo).decode())
        else:
            values.append('')
        values.append(self.company_id.name or '')
        if self.company_id.website:
            values.append(self.company_id.website.replace('http://','').replace('https://',''))
        else:
            values.append('')
        values.append(self.company_id.vat or '')
        values.append(self.company_id.phone or '')
        values.append(self.company_id.company_registry or '')
        values.append(self.name or '')
        values.append(str(self.date_order.strftime('%Y-%m-%d')) or '')
        values.append(self.user_id and self.user_id.partner_id.name or '')
        values.append(self.user_id and self.user_id.partner_id.name or '')
        values.append(self.partner_id and self.partner_id.name or '')
        values.append(self.partner_id and (self.partner_id.vat or '') or '')

        ticket = """
            <div class="pos-sale-ticket">
                <div class="text-center" style="text-align: center !important;">
                    <img src="data:image/png;base64,{}" alt="Logo" style="max-height:2cm; max-width:100%;"/>
                    <br/>
                    <div><strong><h2 class="comp">{}</h2></strong></div>
                    <span>{}</span><br/>
                    <div><span>{} Tel: {}</span></div>
                </div>
                <hr/>
                <div style="text-align: center !important;">
                    {}
                </div>
                <hr/>
                <table>
                    <colgroup>
                        <col width='25%' />
                        <col width='75%' />
                    </colgroup>
                    <tr><td colspan="2">Factura de venta: {}</td></tr>
                    <tr><td>Fecha:</td><td>{}</td></tr>
                    <tr><td>Vendedor:</td><td>{}</td></tr>
                    <tr><td>Cajero:</td><td>{}</td></tr>
                    <tr><td>Cliente:</td><td>{}</td></tr>
                    <tr><td>Cedula:</td><td>{}</td></tr>
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
                    </tr>""".format(*values)
        detalle = ""
        currency = self.pricelist_id.currency_id
        for line in self.lines:
            line_subtotal = "%s%s" %(currency.symbol, str('{:,.0f}'.format(line.price_subtotal))) 
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
                                    """+ str(line.qty)+" X "+str('{:,.0f}'.format(line.price_unit))+"""
                                </line>
                            </left>
                        </td>
                        <td class="pos-right-align">
                            """+line_subtotal+"""
                        </td>
                    </tr>"""
        amount_untaxed = currency.round(sum(line.price_subtotal for line in self.lines))
        totales = """</table>
            <hr/>
            <table class='receipt-total'>
                <tr>
                    <td>BASE:</td>
                    <td class="pos-right-align">
                        """+currency.symbol +" "+ str('{:,.0f}'.format(amount_untaxed))+"""
                    </td>
                </tr>
                <tr>
                    <td>IVA:</td>
                    <td class="pos-right-align">
                        """+currency.symbol +" "+ str('{:,.0f}'.format(self.amount_tax)) +"""
                    </td>
                </tr>
                <tr class="emph">
                    <td>TOTAL:</td>
                    <td class="pos-right-align">
                        """+currency.symbol +" "+ str('{:,.0f}'.format(self.amount_total)) +"""
                    </td>
                </tr>
            </table>
            """
        slogan = """
            <hr/>
            <center>
            <img style="width:300px;height:50px;" alt="Código de barras" src="/report/barcode/?type=Code128&amp;value="""+self.name+"""&amp;width=600&amp;height=100">
            <br/>
            """+self.name+"""
            </center>
            <br/>
            <div style="text-align: center !important;">
                """+self.session_id.config_id.receipt_footer+"""
            </div>
            <br/>
            <center>
            ___________________________
            </center>
            <br/>
            <br/>
            <div style="text-align: center !important;">MUCHAS GRACIAS POR SU VISITA!</div>
            <div style="text-align: center !important;"><span>Impreso con Software POS inCore <a target="_blank" rel="noopener noreferrer" href="https://www.mipos.app">www.mipos.app</a></span></div>
            """
        
        text_val = ticket + detalle + totales + slogan
        res = {"name":text_val,}
        wizard_id = self.env['pos.print.receipt'].create(res)
        view_id = self.env.ref('pos_receipt_note_2.pos_print_receipt_form').id

        context = self._context.copy()
        return {
            'name':'Print Receipt',
            'view_type':'form',
            'view_mode':'tree',
            'views' : [(view_id,'form')],
            'res_model':'pos.print.receipt',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':wizard_id.id,
            'target':'new',
            'context':context,

        }
