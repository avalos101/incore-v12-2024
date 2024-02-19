# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from incore import fields, models


class ResPartner(models.Model):
    """Informacion extra en el cliente"""
    _inherit = 'res.partner'

    start_date = fields.Date('Fecha de inicio')
    domain_name = fields.Char('Dominio')
    user_name = fields.Char('Usuario')
    system_version = fields.Selection(
        [('12', '12.0'), ('11', '11.0'), ('10', '10.0')], string='Version de inCore')
    server_id = fields.Many2one(
        'partner_extra_technical_data.server', string="Servidor")
    product_ids = fields.Many2many(
        'product.product', string="Productos asociados")
