import incore.tests
# @incore.tests.common.at_install(False)
# @incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):
    def test_01_ui(self):
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('activity_creation')", "incore.__DEBUG__.services['web_tour.tour'].tours.activity_creation.ready", login='admin')

    def test_02_ui(self):
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('test_screen_navigation')", "incore.__DEBUG__.services['web_tour.tour'].tours.test_screen_navigation.ready", login='admin')
