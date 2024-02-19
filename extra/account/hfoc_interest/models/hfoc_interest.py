from incore import models, fields, api, _
from incore.exceptions import UserError, Warning
import pytz
from datetime import datetime, timedelta, date, time
import json


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    hfoc_inicial = fields.Boolean(string='Es una inicial?',  copy=False)

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    product_interest = fields.Many2one('product.product', string='Producto Financiamiento')
    porcentaje_interes = fields.Float(string='Tasa %',  copy=False)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    inicial_estimada = fields.Float(string='Inicial estimada', copy=False)
    aux_interes = fields.Float(string='Aux', copy=False)
    cronograma = fields.Html(string='Cronograma', compute='info_html', copy=False)
    cronograma2 = fields.Html(string='Cronograma', compute='info_html', copy=False)
    date_financing = fields.Date(string='Fecha de financiación',
        readonly=True, states={'draft': [('readonly', False)]}, index=True,
        help="Keep empty to use the current date", copy=False)


    @api.one
    def calcular_linea_interes(self):
        self.payment_term_id.product_interest.taxes_id
        self.payment_term_id.porcentaje_interes
        total = 0
        for sun in self.invoice_line_ids:
            if sun.product_id.id != self.payment_term_id.product_interest.id:
                line_total = 0
                line_total = sun.price_unit*sun.quantity
                total += line_total-(line_total*((sun.discount/100)+1)-line_total)
        self.comment = str(total)
        interes = 0.0
        interes_first = (self.payment_term_id.porcentaje_interes*(self.amount_total-self.inicial_estimada))/100
        aux = 0
        for line in self.invoice_line_ids:
            if line.product_id.id == self.payment_term_id.product_interest.id:
                interes = (self.payment_term_id.porcentaje_interes*(total-self.inicial_estimada))/100
                line.update({'price_unit': interes})
                self.aux_interes = interes
                aux = 1

        self._onchange_invoice_line_ids()
        if aux == 0:
            vals = {
                "product_id": self.payment_term_id.product_interest.id or "",
                "name": 'Financiamiento %' + str(self.payment_term_id.porcentaje_interes) ,
                "account_id": 175,
                "price_unit": interes_first,
            }

            self.invoice_line_ids = self.invoice_line_ids + self.invoice_line_ids.create(vals)
            self.aux_interes = interes_first
        if self.payment_term_id.product_interest.id:
            for tax in self.invoice_line_ids:
                if tax.product_id.id == self.payment_term_id.product_interest.id:
                    if not tax.invoice_line_tax_ids:
                        tax.invoice_line_tax_ids = self.payment_term_id.product_interest.taxes_id or ""
                        self._onchange_invoice_line_ids()

    @api.one
    def info_html(self):
        if not self.date_financing:
            self.date_financing = self.date_invoice or fields.Date.today()
        if self.date_financing:
            head = """ <table class="o_list_view table table-condensed table-striped o_list_view_ungrouped" id="cronograma">
                        <tr style="background: #4b616c; color: white;" >
                            <th>N° Cuota</th>
                            <th>Fecha</th>
                            <th>Valor Cuota</th>
                        </tr>
                    """
            head2 = """ <table cellpadding="4" border="1" id="cronograma2">
                        <tr style= >
                            <th>N° Cuota</th>
                            <th>Fecha</th>
                            <th>Valor Cuota</th>
                        </tr>
                    """
            end = """
                        </table>"""

            content = numero = fecha = couta = ''
            date_format = '%Y-%m-%d'
            date_financing = datetime.strptime(str(self.date_financing), date_format)
            count = 0
            sum_couta = 0.0
            value_cuota = 0.0

            if len(self.payment_term_id.line_ids) > 0:
                for line in self.payment_term_id.line_ids:
                    count = count + 1
                    numero = "<tr><td> "+ str(count) + "</td>"
                    fecha = "<td>" + str((date_financing + timedelta(days=line.days) ).strftime(date_format)) +"</td>"
                    if line.value == 'percent':
                        value_cuota = (line.value_amount*(self.amount_total-self.inicial_estimada))/100
                        couta = "<td>" '$'+ str('{:,.0f}'.format(round(value_cuota, -2))) + "</td></tr>"
                        sum_couta = sum_couta + value_cuota
                    elif line.value == 'fixed':
                        value_cuota = line.value_amount
                        couta = "<td>" '$'+ str('{:,.0f}'.format(round(value_cuota, -2))) + "</td></tr>"
                        sum_couta = sum_couta + value_cuota
                    elif line.value == 'balance':
                        value_cuota = (self.amount_total-self.inicial_estimada) - sum_couta
                        couta = "<td>" '$'+ str('{:,.0f}'.format(round(value_cuota, -2))) + "</td></tr>"
                    content = content + numero + fecha + couta
            self.cronograma = head + content + end

            if len(self.payment_term_id.line_ids) > 1:
                self.cronograma2 = "<strong>Cronograma</strong><br></br>"+head2 + content + end
            else:
                self.cronograma2 = ""
