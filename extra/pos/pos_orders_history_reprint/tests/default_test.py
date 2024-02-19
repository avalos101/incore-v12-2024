import incore.tests


@incore.tests.common.at_install(True)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):

    def test_01_pos_is_loaded(self):
        self.phantom_js(
            '/web',

            "incore.__DEBUG__.services['web_tour.tour']"
            ".run('pos_orders_history_reprint_tour')",

            "incore.__DEBUG__.services['web_tour.tour']"
            ".tours.pos_orders_history_reprint_tour.ready",

            login="admin",
            timeout=240,
        )
