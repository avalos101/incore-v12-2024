import incore.tests


@incore.tests.common.at_install(True)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):

    def test_01_pos_is_loaded(self):
        env = self.env
        # needed because tests are run before the module is marked as
        # installed. In js web will only load qweb coming from modules
        # that are returned by the backend in module_boot. Without
        # this you end up with js, css but no qweb.
        env['ir.module.module'].search([('name', '=', 'pos_cashier_select')], limit=1).state = 'installed'

        self.phantom_js(
            '/web',

            "incore.__DEBUG__.services['web_tour.tour']"
            ".run('pos_cashier_select_tour')",

            "incore.__DEBUG__.services['web_tour.tour']"
            ".tours.pos_cashier_select_tour.ready",

            login="admin",
            timeout=240,
        )
