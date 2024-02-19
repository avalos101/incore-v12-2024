# -*- coding: utf-8 -*-

from incore import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _order = 'sequence, barcode, name, id'

    barcode = fields.Char('Internal Reference', index=True, default=lambda self: _('New'), copy=False)
    barcode_index = fields.Integer('Internal Reference Index', readonly=True, default=0)

    _sql_constraints = [
        ('uniq_barcode',
         'unique(barcode)',
         'The reference must be unique. Try save again.'),
    ]

    @api.model
    def default_get(self, fields):
        context = self._context or {}
        res = super(ProductProduct, self).default_get(fields)

        if 'categ_id' in res:
            self._onchange_categ_id()
        return res

    @api.model
    def create(self, vals):
        code_index = 0
        cat = None
        if 'categ_id' in vals:
            cat = self.env['product.category'].search([('id', '=', vals['categ_id'])], limit=1)
        if 'barcode' not in vals or vals['barcode'] == _('New'):
            if 'product_tmpl_id' in vals:
                template = self.env['product.template'].search([('id', '=', vals['product_tmpl_id'])], limit=1)
                if template.barcode and template.barcode != '':
                    code_stored = template.barcode
                else:
                    code_stored = template.barcode_index
                if not code_stored:
                    code_stored = ''
                mylen = len(template.product_variant_ids)
                try:
                    attr = vals['attribute_value_ids'][0][2]
                except:
                    attr = 0


                if self.env.context.get('create_from_tmpl') and not (attr):
                    code_index = 0
                    vals['barcode_index'] = code_index
                    vals['barcode'] = code_stored
                elif mylen == 0:

                    code_index = 1
                    vals['barcode_index'] = code_index
                    vals['barcode'] = code_stored + '%05d' % (code_index)
                elif mylen == 1:

                    code_index = template.product_variant_ids[:1].barcode_index
                    if template.product_variant_ids[:1].attribute_value_ids:
                        if code_index == 0:
                            code_index = 1
                        template.product_variant_ids[:1].barcode_index = code_index
                        template.product_variant_ids[:1].barcode = code_stored + '%05d' % (code_index)

                    code_index = code_index + 1
                    vals['barcode_index'] = code_index
                    vals['barcode'] = code_stored + '%05d' % (code_index)
                elif mylen > 1:

                    variant_max = max(template.product_variant_ids, key=lambda x: x['barcode_index'])
                    code_index = variant_max['barcode_index'] + 1
                    vals['barcode_index'] = code_index
                    vals['barcode'] = code_stored + '%05d' % (code_index)
                else:

                    variant_max = max(template.product_variant_ids, key=lambda x: x['barcode_index'])
                    code_index = variant_max['barcode_index'] + 1
                    vals['barcode_index'] = code_index
                    vals['barcode'] = code_stored + '%05d' % (code_index)
            else:

                sequence = self.env.ref('app_product_auto_code.seq_product_default', raise_if_not_found=False)
                if cat and cat.product_sequence:
                    sequence = cat.product_sequence
                try:
                    vals['barcode'] = sequence.next_by_id()
                except:
                    pass
        else:
            pass
        if cat and cat.barcode_auto and vals['barcode']:
            vals['barcode'] = vals['barcode']
        if vals.get('barcode'):
            vals['default_code'] = vals['barcode']
        return super(ProductProduct, self).create(vals)

    # @api.multi
    # def write(self, vals):
    #     cat = None
    #     _logger.info('\n\n %r \n\n', self)
    #     _logger.info('\n\n %r \n\n', vals)
    #     if 'categ_id' in vals:
    #         cat = self.env['product.category'].search([('id', '=', vals['categ_id'])], limit=1)
    #     else:
    #         cat = self.categ_id

    #     if vals.get('barcode') or self.barcode == _('New'):
    #         seq = False
    #         if vals.get('barcode') and vals.get('barcode') == _('New'):
    #             seq = True
    #         if not vals.get('barcode') and self.barcode == _('New'):
    #             seq = True
    #         if vals.get('barcode') == self.barcode == _('New'):
    #             seq = True

    #         if seq:
    #             sequence = self.env.ref('app_product_auto_code.seq_product_default', raise_if_not_found=False)
    #             if cat and cat.product_sequence:
    #                 sequence = cat.product_sequence
    #             try:
    #                 vals['barcode'] = sequence.next_by_id()
    #             except:
    #                 pass
    #     else:
    #         pass
    #     if cat and cat.barcode_auto and vals.get('barcode'):
    #         vals['barcode'] = vals['barcode']
    #     if vals.get('barcode'):
    #         vals['default_code'] = vals['barcode']
    #     return super(ProductProduct, self).write(vals)


    @api.multi
    def copy(self, default=None):
        if len(self.product_tmpl_id.product_variant_ids) > 1:
            raise exceptions.ValidationError(_('Product varient can only create in Product view!'))
        return super(ProductProduct, self).copy(default=None)

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id:
            self.type = self.categ_id.type
            self.rental = self.categ_id.rental
            self.sale_ok = self.categ_id.sale_ok
            self.purchase_ok = self.categ_id.purchase_ok
            self.tracking = self.categ_id.tracking
