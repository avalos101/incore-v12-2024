# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import http
from incore.http import request
from incore.addons.portal.controllers.web import Home


class WebsiteTest(Home):

    @http.route('/test_view', type='http', auth="public", website=True)
    def test_view(self, **kw):
        return request.render('test_website.test_view')
