# -*- coding: utf-8 -*-
from incore import http, _
from incore.http import request
from incore.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

	def _get_mandatory_billing_fields(self):
		required_fields = super()._get_mandatory_billing_fields()
		required_fields += ['vat','last_name']
		return required_fields

	def _get_mandatory_shipping_fields(self):
		required_fields = super()._get_mandatory_shipping_fields()
		required_fields += ['vat','last_name']
		return required_fields

	def values_preprocess(self, order, mode, values):
		res = super().values_preprocess(order=order, mode=mode, values=values)
		res['lat_name'] = res.get('last_name','')
		return res