import incore.tests
# Part of incore. See LICENSE file for full copyright and licensing details.


@incore.tests.tagged('post_install', '-at_install')
class TestUi(incore.tests.HttpCase):

    def test_01_free_delivery_when_exceed_threshold(self):
        self.env.ref("delivery.free_delivery_carrier").write({
            'fixed_price': 2,
            'free_over': True,
            'amount': 10,
        })
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('check_free_delivery')", "incore.__DEBUG__.services['web_tour.tour'].tours.check_free_delivery.ready", login="admin")
