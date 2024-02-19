import incore.tests


@incore.tests.common.at_install(False)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):

    def test_01_pos_is_loaded(self):
        self.phantom_js(
            '/web?debug=assets',

            "incore.__DEBUG__.services['web_tour.tour']"
            ".run('pos_orderline_absolute_discount_tour')",

            "incore.__DEBUG__.services['web_tour.tour']"
            ".tours.pos_orderline_absolute_discount_tour.ready",

            login="admin",
            timeout=240,
        )
