# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
import incore.tests


@incore.tests.tagged('post_install', '-at_install')
class TestUi(incore.tests.HttpCase):
    def test_01_portal_load_tour(self):
        self.phantom_js(
            "/",
            "incore.__DEBUG__.services['web_tour.tour'].run('portal_load_homepage')",
            "incore.__DEBUG__.services['web_tour.tour'].tours.portal_load_homepage.ready",
            login="portal"
        )
