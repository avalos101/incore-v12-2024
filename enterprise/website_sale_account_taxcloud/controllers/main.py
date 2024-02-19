# -*- coding: utf-8 -*-

from incore import http
from incore.http import request

from incore.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        response = super(WebsiteSale, self).payment(**post)
        order = request.website.sale_get_order()
        if order.fiscal_position_id.is_taxcloud:
            order.validate_taxes_on_sales_order()

        return response
