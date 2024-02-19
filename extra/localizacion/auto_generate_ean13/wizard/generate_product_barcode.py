# -*- coding: utf-8 -*-
from incore import api, fields, models


class GenerateProductBarcode(models.TransientModel):
    _name = 'generate.product.barcode'

    override_barcode = fields.Boolean('Override Existing Barcode')

    @api.multi
    def generate_barcode(self):
        if self._context.get('active_model') == 'product.template' and self._context.get('active_ids'):
            ctx = dict(self._context)
            for obj in self:
                if obj.override_barcode:
                    ctx.update({'override_barcode': True})
                self.env['product.template'].browse(self._context.get('active_ids')).with_context(ctx).generate_barcode()
        return True
