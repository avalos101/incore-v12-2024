# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import incore.tests


@incore.tests.tagged('post_install','-at_install')
class TestUi(incore.tests.HttpCase):
    def test_ui(self):
        self.phantom_js("/web", "incore.__DEBUG__.services['web_tour.tour'].run('account_followup_reports_widgets')", "incore.__DEBUG__.services['web_tour.tour'].tours.account_followup_reports_widgets.ready", login='admin')
