# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import http
from incore.http import request


class ImSupport(http.Controller):

    @http.route('/im_support/tests', type='http', auth="user")
    def test_suite(self, mod=None, **kwargs):
        return request.render('im_support.support_qunit_suite')
