# Part of inCore. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-

import incore.tests


@incore.tests.tagged('post_install','-at_install')
class TestUi(incore.tests.HttpCase):
    def test_ui(self):
        self.phantom_js("/web", "incore.__DEBUG__.services['web_tour.tour'].run('helpdesk_tour')", ready="incore.__DEBUG__.services['web_tour.tour'].tours.helpdesk_tour.ready", login="admin")
