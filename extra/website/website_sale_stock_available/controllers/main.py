# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore.http import request, route
from incore.addons.incore_customize.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super().shop(
            page=page, category=category, search=search, ppg=ppg, **post)
        all_products = res.qcontext.get('products')
        products_availables = all_products.get_only_availables()
        new_bins = request.env['product.template'].get_bins(
            products_availables)
        res.qcontext.update({
            'products': products_availables,
            'bins': new_bins,
        })
        return res

