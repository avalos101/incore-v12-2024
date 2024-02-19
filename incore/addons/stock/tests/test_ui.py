# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import incore.tests

@incore.tests.tagged('post_install', '-at_install')
class TestUi(incore.tests.HttpCase):

    def test_01_admin_stock_route(self):
        self.phantom_js("/web", "incore.__DEBUG__.services['web_tour.tour'].run('stock')", "incore.__DEBUG__.services['web_tour.tour'].tours.stock.ready", login='admin')
