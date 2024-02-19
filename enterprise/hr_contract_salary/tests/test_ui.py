# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import incore.tests


@incore.tests.common.at_install(False)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):
    def test_ui(self):
        self.phantom_js(
            "/",
            "incore.__DEBUG__.services['web_tour.tour'].run('hr_contract_salary_tour', 'test')",
            "incore.__DEBUG__.services['web_tour.tour'].tours.hr_contract_salary_tour.ready", login='admin',
            timeout=100)
