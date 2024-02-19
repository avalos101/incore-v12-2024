# -*- coding: utf-8 -*-
import logging
import re

from incore import models, fields, api
from incore.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    fe_habilitada = fields.Boolean(
        string='Habilitar'
    )

    fe_primer_apellido = fields.Char(
        string='Primer apellido',
    )
    fe_primer_nombre = fields.Char(
        string='Primer nombre',
    )
    fe_segundo_nombre = fields.Char(
        string='Segundo nombre',
        default=''
    )
    fe_tipo_documento = fields.Selection(
        (
            ('11', 'Registro civil'),
            ('12', 'Tarjeta de identidad'),
            ('13', 'Cédula de ciudadanía'),
            ('21', 'Tarjeta de extranjería'),
            ('22', 'Cédula de extranjería'),
            ('31', 'NIT'),
            ('41', 'Pasaporte'),
            ('42', 'Documento de identificación extranjero'),
            ('50', 'NIT de otro país'),
            ('91', 'NUIP'),
        ),
        'Tipo de documento',
        default='31',
    )
    fe_nit = fields.Char(
        string='NIT',
    )
    fe_digito_verificacion = fields.Char(
        string='Dígito de verificación',
    )
    fe_es_compania = fields.Selection(
        (
            ('1', 'Jurídica'),
            ('2', 'Natural'),
        ),
        'Tipo de persona',
        default='1',
    )
    fe_tipo_regimen = fields.Selection(
        (
            ('00', 'Simplificado'),
            ('02', 'Común'),
            ('03', 'No aplicable'),
            ('04', 'Simple'),
            ('05', 'Ordinario')
        ),
        'Tipo de régimen',
        default='04',
    )
    fe_es_contribuyente = fields.Boolean(
        string='Gran contribuyente'
    )
