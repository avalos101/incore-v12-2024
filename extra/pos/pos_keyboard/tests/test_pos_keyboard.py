# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/kolushovalexandr>
# License MIT (https://opensource.org/licenses/MIT).

import incore.tests


@incore.tests.common.at_install(True)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):
    def test_pos_keyboard(self):
        # without a delay there might be problems on the steps whilst opening a POS
        # caused by a not yet loaded button's action
        self.phantom_js(
            "/web",
            "incore.__DEBUG__.services['web_tour.tour'].run('pos_keyboard_tour', 500)",
            "incore.__DEBUG__.services['web_tour.tour'].tours.pos_keyboard_tour.ready",
            login="admin",
        )
