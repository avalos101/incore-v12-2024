# -*- coding: utf-8 -*-

from incore import models, fields, api, exceptions, _
class ProductProduct(models.Model):
    _inherit = 'product.product'

    supplier_code = fields.Char('Codigo Proveedor', index=True)

    @api.model
    def create(self, vals):
        if 'product_tmpl_id' in vals:
            template = self.env['product.template'].search([('id', '=', vals['product_tmpl_id'])], limit=1)
            mylen = len(template.product_variant_ids)
            if mylen > 1:
                vals['supplier_code'] = template.product_variant_ids[0].supplier_code
            if template.supplier_code:
                vals['supplier_code'] = template.supplier_code
        return super(ProductProduct, self).create(vals)