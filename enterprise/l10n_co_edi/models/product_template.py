# coding: utf-8
from incore import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_co_edi_brand = fields.Char(string='Brand', help='Reported brand in the Colombian electronic invoice.')
