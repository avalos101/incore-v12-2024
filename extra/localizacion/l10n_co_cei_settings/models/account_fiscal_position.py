# -*- coding: utf-8 -*-
import logging

from incore import models, fields, api

_logger = logging.getLogger(__name__)


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    fe_codigo_dian = fields.Selection(
        (
            ('0', 'Simplificado'),
            ('2', 'Común'),
        ),
        'Código DIAN',
        required=False
    )
