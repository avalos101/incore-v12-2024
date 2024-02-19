# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
from incore import fields, models


class EasypostService(models.Model):
    _name = 'easypost.service'
    _description = 'Easypost Service'

    name = fields.Char('Service Level Name', index=True)
    easypost_carrier = fields.Char('Carrier Prefix', index=True)
