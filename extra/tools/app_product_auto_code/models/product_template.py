# -*- coding: utf-8 -*-

from incore import api, fields, models, exceptions, _
class ProductTemplate(models.Model):
    _inherit = ['product.template']
    _order = "sequence, name"

    barcode = fields.Char(
        'Internal Reference',
        compute='_compute_default_barcode',
        inverse='_set_default_barcode',
        related=None,
        store=True, default=lambda self: _('New'), copy=False)
    barcode_index = fields.Char('Internal Reference Stored',
                                      default=lambda self: _('New'))

    _sql_constraints = [
        ('uniq_default_code',
         'CHECK(1=1)',
         'The reference must be unique. Try save again.'),
    ]

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplate, self).default_get(fields)
        if 'categ_id' in res:
            self._onchange_categ_id()
        return res

    @api.model
    def create(self, vals):
        cat = None
        if 'categ_id' in vals:
            cat = self.env['product.category'].search([('id', '=', vals['categ_id'])], limit=1)
        if 'attribute_line_ids' in vals:
            if len(vals['attribute_line_ids']) > 0:
                raise exceptions.ValidationError(_('Please save product first before adding varients!'))

        if 'barcode' not in vals or vals['barcode'] == _('New'):
            sequence = self.env.ref('app_product_auto_code.seq_product_default', raise_if_not_found=False)
            if cat and cat.product_sequence:
                sequence = cat.product_sequence
            try:
                vals['barcode'] = sequence.next_by_id()
            except:
                pass
        else:
            pass

        if vals['barcode']:
            vals['barcode_index'] = vals['barcode']

        if cat and cat.barcode_auto and vals['barcode']:
            vals['barcode'] = vals['barcode']
        if vals.get('barcode'):
            vals['default_code'] = vals['barcode']
        return super(ProductTemplate, self).create(vals)
    @api.multi
    def write(self, vals):
        cat = None
        if 'categ_id' in vals:
            cat = self.env['product.category'].search([('id', '=', vals['categ_id'])], limit=1)
        else:
            cat = self.categ_id

        if vals.get('barcode') or self.barcode == _('New'):
            seq = False
            if vals.get('barcode') and vals.get('barcode') == _('New'):
                seq = True
            if not vals.get('barcode') and self.barcode == _('New'):
                seq = True
            if vals.get('barcode') == self.barcode == _('New'):
                seq = True

            if seq:
                sequence = self.env.ref('app_product_auto_code.seq_product_default', raise_if_not_found=False)
                if cat and cat.product_sequence:
                    sequence = cat.product_sequence
                try:
                    vals['barcode'] = sequence.next_by_id()
                except:
                    pass
        else:
            pass
        if vals.get('barcode'):
            vals['barcode_index'] = vals['barcode']
        if cat and cat.barcode_auto and vals.get('barcode'):
            vals['barcode'] = vals['barcode']
        if vals.get('barcode'):
            vals['default_code'] = vals['barcode']
        return super(ProductTemplate, self).write(vals)


    @api.depends('product_variant_ids', 'product_variant_ids.barcode')
    def _compute_default_barcode(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)

        for template in unique_variants:
            template.barcode = template.product_variant_ids.barcode
        for template in (self - unique_variants):
            if len(template.product_variant_ids) > 1 and template.barcode_index:
                template.barcode = template.barcode_index
                # template.barcode = ''

    @api.one
    def _set_default_barcode(self):
        if self.barcode:
            self.barcode_index = self.barcode
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.barcode = self.barcode_index

    @api.depends('product_variant_ids', 'product_variant_ids.barcode')
    def _compute_default_code(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            # template.default_code = template.product_variant_ids.default_code
            template.default_code = template.product_variant_ids.barcode
        for template in (self - unique_variants):
            template.default_code = template.barcode_index
            # template.default_code = ''

    @api.one
    def _set_default_code(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.default_code = self.barcode_index


    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id:
            self.type = self.categ_id.type
            self.rental = self.categ_id.rental
            self.sale_ok = self.categ_id.sale_ok
            self.purchase_ok = self.categ_id.purchase_ok
            self.tracking = self.categ_id.tracking
