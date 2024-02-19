# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).

import incore.tests


@incore.tests.common.at_install(True)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):
    def test_pos_debt(self):
        # without a delay there might be problems caused by a not yet loaded button's action
        self.phantom_js(
            "/web",
            "incore.__DEBUG__.services['web_tour.tour'].run('tour_pos_debt_notebook', 1000)",
            "incore.__DEBUG__.services['web_tour.tour'].tours.tour_pos_debt_notebook.ready",
            login="admin",
            timeout=1000,
        )
