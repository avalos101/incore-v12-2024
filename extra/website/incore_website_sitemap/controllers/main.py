# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from incore import http, SUPERUSER_ID
from incore.http import request


class incoreWebsiteSitemap(http.Controller):

    @http.route(['/page/sitemap'], type='http', auth="public", website=True)
    def incore_sitemap(self, page=0, category=None, search='', **post):
    	cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
    	
    	return request.render("incore_website_sitemap.website_sitemap")
    	
    	       
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
