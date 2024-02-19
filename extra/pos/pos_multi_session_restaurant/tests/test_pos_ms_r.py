# Copyright 2017  <https://incore.co/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import incore.tests


@incore.tests.common.at_install(False)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):

    def test_pos_ms_r(self):
        # without a delay there might be problems on the steps whilst opening a POS
        # caused by a not yet loaded button's action
        self.phantom_js("/web", "incore.__DEBUG__.services['web_tour.tour'].run('open_pos_ms_r_tour')",
                        "incore.__DEBUG__.services['web_tour.tour'].tours.open_pos_ms_r_tour.ready",
                        login="admin")
