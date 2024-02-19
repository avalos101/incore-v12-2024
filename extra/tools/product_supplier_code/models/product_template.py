# -*- coding: utf-8 -*-

from incore import api, fields, models, exceptions, _
class ProductTemplate(models.Model):
    _inherit = ['product.template']

    supplier_code = fields.Char(u'Código Proveedor', 
        compute='_compute_supplier_code',
        inverse='_set_supplier_code', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.supplier_code')
    def _compute_supplier_code(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.supplier_code = template.product_variant_ids.supplier_code
        for template in (self - unique_variants):
            if len(template.product_variant_ids):
                template.supplier_code = template.product_variant_ids[0].supplier_code

    @api.one
    def _set_supplier_code(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.supplier_code = self.supplier_code

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if vals.get('supplier_code'):
            res.write({'supplier_code':vals['supplier_code']})
        return res