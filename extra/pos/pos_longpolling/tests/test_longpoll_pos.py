import incore.tests


@incore.tests.common.at_install(False)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):

    def test_longpolling_pos(self):
        # without a delay there might be problems on the steps whilst opening a POS
        # caused by a not yet loaded button's action
        self.phantom_js("/web",
                        "incore.__DEBUG__.services['web_tour.tour'].run('longpoll_connection_tour')",
                        "incore.__DEBUG__.services['web_tour.tour'].tours.longpoll_connection_tour.ready",
                        login="admin")
