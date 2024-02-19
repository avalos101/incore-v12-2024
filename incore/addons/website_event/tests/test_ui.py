import incore.tests


@incore.tests.tagged('post_install', '-at_install')
class TestUi(incore.tests.HttpCase):
    def test_admin(self):
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('event')", "incore.__DEBUG__.services['web_tour.tour'].tours.event.ready", login='admin')
