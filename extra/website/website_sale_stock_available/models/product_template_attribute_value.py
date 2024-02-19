# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import api, models


class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    def _is_variant_available(self):
        """Check if there is any variant available in stock
        with the attribute value requested."""
        self.ensure_one()
        template = self.product_tmpl_id
        if template.not_show_variants:
            attribute_value_id = self.product_attribute_value_id.id
            variants_availables = template.product_variant_ids.filtered(
                lambda variant: variant.sudo().virtual_available > 0 and
                attribute_value_id in variant.attribute_value_ids.mapped('id'))
            return any(variants_availables)
        return True

    @api.multi
    def _is_variant_available_all(self):
        template = self.mapped('product_tmpl_id')
        template.ensure_one()
        attribute_value_ids = self.mapped('product_attribute_value_id.id')
        variant_available = template.product_variant_ids.filtered(
            lambda variant: variant.sudo().virtual_available > 0 and
            attribute_value_ids == variant.attribute_value_ids.mapped('id'))
        return variant_available
