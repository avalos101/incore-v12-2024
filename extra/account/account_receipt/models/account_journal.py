# -*- coding: utf-8 -*-

from incore import api, fields, models, tools, _

class AccountJournal(models.Model):
    _inherit = "account.journal"

    report_header = fields.Text(string="Encabezado")
    report_footer = fields.Text(string=u"Pié de página")