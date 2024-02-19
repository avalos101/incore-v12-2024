# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore.http import request, route
from incore.addons.sale.controllers.product_configurator import ProductConfiguratorController


class ProductConfiguratorController(ProductConfiguratorController):

    @route()
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        res = super().get_combination_info(
            product_template_id=product_template_id,
            product_id=product_id,
            combination=combination,
            add_qty=add_qty,
            pricelist_id=pricelist_id,
            **kw)
        if res.get('product_template_id'):
            product_template = request.env['product.template'].browse(
                res['product_template_id'])
            res.update({
                'product_template_virtual_available':
                product_template.sudo().virtual_available,
                'product_variant_count':
                product_template.product_variant_count,
            })

        return res
