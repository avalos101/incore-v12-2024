# -*- coding: utf-8 -*-
# Part of incore. See LICENSE file for full copyright and licensing details.
import incore.tests


@incore.tests.common.at_install(False)
@incore.tests.common.post_install(True)
class TestUi(incore.tests.HttpCase):
    def test_01_wishlist_tour(self):
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('shop_wishlist')", "incore.__DEBUG__.services['web_tour.tour'].tours.shop_wishlist.ready")
