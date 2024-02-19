# Copyright 2018  <https://incore.co/team/KolushovAlexandr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import incore.tests


@incore.tests.common.at_install(True)
@incore.tests.common.post_install(True)
class TestUI(incore.tests.HttpCase):

    def test_pos_product_available_negative(self):
        # needed because tests are run before the module is marked as
        # installed. In js web will only load qweb coming from modules
        # that are returned by the backend in module_boot. Without
        # this you end up with js, css but no qweb.
        env = self.env
        env['ir.module.module'].search([('name', '=', 'pos_product_available')], limit=1).state = 'installed'

        env['product.template'].search([('name', '=', 'Yellow Peppers')]).write({
            'type': 'product',
        })

        # without a delay there might be problems caused by a not yet loaded button's action
        self.phantom_js("/web",
                        "incore.__DEBUG__.services['web_tour.tour'].run('tour_pos_product_available_negative', 500)",
                        "incore.__DEBUG__.services['web_tour.tour'].tours.tour_pos_product_available_negative.ready",
                        login="admin", timeout=150)
