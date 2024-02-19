# -*- coding: utf-8 -*-

from incore import api, fields, models


class WebsiteProductCategory(models.Model):
    _inherit = 'product.public.category'
    
    description = fields.Html('Description for Category', translate=True)
