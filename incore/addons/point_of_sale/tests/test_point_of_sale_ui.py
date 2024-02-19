# Part of incore. See LICENSE file for full copyright and licensing details.

import incore.tests


@incore.tests.tagged('post_install', '-at_install')
class TestUi(incore.tests.HttpCase):

    def test_01_point_of_sale_tour(self):
        self.phantom_js("/web", "incore.__DEBUG__.services['web_tour.tour'].run('point_of_sale_tour')", "incore.__DEBUG__.services['web_tour.tour'].tours.point_of_sale_tour.ready", login="admin")
