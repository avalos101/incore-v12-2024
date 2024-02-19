# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import incore.tests

@incore.tests.tagged('post_install', '-at_install')
class TestUi(incore.tests.HttpCase):

    def test_01_admin_rte(self):
        self.phantom_js("/web", "incore.__DEBUG__.services['web_tour.tour'].run('rte')", "incore.__DEBUG__.services['web_tour.tour'].tours.rte.ready", login='admin')

    def test_02_admin_rte_inline(self):
        self.phantom_js("/web", "incore.__DEBUG__.services['web_tour.tour'].run('rte_inline')", "incore.__DEBUG__.services['web_tour.tour'].tours.rte_inline.ready", login='admin')
