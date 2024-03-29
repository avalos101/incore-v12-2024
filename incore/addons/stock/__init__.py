# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models
from . import report
from . import wizard


from incore import api, SUPERUSER_ID


# TODO: Apply proper fix & remove in master
def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.model.data'].search([
        ('model', 'like', '%stock%'),
        ('module', '=', 'stock')
    ]).unlink()

def _create_warehouse(cr, registry):
    """ This hook is used to add a warehouse on existing companies
    when module stock is installed.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    company_ids  = env['res.company'].search([])
    company_with_warehouse = env['stock.warehouse'].search([]).mapped('company_id')
    company_without_warehouse = company_ids - company_with_warehouse
    for company in company_without_warehouse:
        company.create_transit_location()
        env['stock.warehouse'].create({
            'name': company.name,
            'code': company.name[:5],
            'company_id': company.id,
            'partner_id': company.partner_id.id
        })
