# Part of inCore. See LICENSE file for full copyright and licensing details.

import incore.tests


@incore.tests.tagged('post_install', '-at_install')
class TestUi(incore.tests.HttpCase):

    def test_01_project_tour(self):
        self.phantom_js("/web", "incore.__DEBUG__.services['web_tour.tour'].run('mail_tour')", "incore.__DEBUG__.services['web_tour.tour'].tours.mail_tour.ready", login="admin")
