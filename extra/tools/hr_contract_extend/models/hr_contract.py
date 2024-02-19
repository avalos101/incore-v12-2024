# -*- coding: utf-8 -*-

from incore import api, fields, models, tools, _

class HrContract(models.Model):
    _inherit = 'hr.contract'

    employee_eps = fields.Char(string='EPS')
    employee_afp = fields.Char(string='Pensiones')
    employee_afc = fields.Char(string='Cesantías')
    employee_arl = fields.Char(string='Riesgos laborales')
    employee_compensation = fields.Char(string='Caja de compensación')
