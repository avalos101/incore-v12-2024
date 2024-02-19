# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import fields, models, api
from incore.addons.website_sale.controllers.main import TableCompute


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inventory_availability = fields.Selection(selection_add=[
        ('not_show', 'Not show the product variants if it is not available.')])
    not_show_variants = fields.Boolean(
        compute='_compute_not_show_variants')

    @api.model
    def not_show_variants_unavailable(self):
        ir_default = self.env['ir.default'].sudo()
        setting_inventory_availability = ir_default.get(
            'product.template', 'inventory_availability')
        not_show = setting_inventory_availability == 'not_show'
        return not_show

    @api.depends('inventory_availability')
    def _compute_not_show_variants(self):
        """Compute value of field not_show_variants."""
        for record in self:
            if record.inventory_availability:
                record.not_show_variants = (
                    record.inventory_availability == 'not_show')
            else:
                record.not_show_variants == (
                    self.not_show_variants_unavailable())

    @api.multi
    def get_only_availables(self):
        """Returns only the products available in stock."""
        not_show = self.not_show_variants_unavailable()
        if not_show:
            return self.filtered(
                lambda product: not product.not_show_variants
                or ((product.not_show_variants or not product.inventory_availability)
                    and product.sudo().virtual_available > 0))

        return self.filtered(
            lambda product: not product.not_show_variants
            or not product.inventory_availability
            or (product.not_show_variants and product.sudo().virtual_available > 0))

    @api.model
    def get_bins(self, products):
        """Build bins and return it."""
        return TableCompute().process(products)

    def _get_first_possible_combination(self, parent_combination=None, necessary_values=None):
        first_possible_combination = super()._get_first_possible_combination(
            parent_combination=parent_combination,
            necessary_values=necessary_values)
        if self.not_show_variants and self.sudo().virtual_available > 0:
            if len(self.product_variant_ids) > 1:
                first_possible_combination_available = False
                possible_combinations = self._get_possible_combinations(
                    parent_combination, necessary_values)
                while not first_possible_combination_available:
                    first_possible_combination = next(
                        possible_combinations,
                        self.env['product.template.attribute.value'])

                    if first_possible_combination._is_variant_available_all():
                        first_possible_combination_available = True
        return first_possible_combination
