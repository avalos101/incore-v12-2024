# Part of inCore. See LICENSE file for full copyright and licensing details.

import incore.tests


@incore.tests.tagged('click_all', 'post_install', '-at_install', '-standard')
class TestMenusAdmin(incore.tests.HttpCase):

    def test_01_click_everywhere_as_admin(self):
        self.browser_js("/web", "incore.__DEBUG__.services['web.clickEverywhere']();", "incore.isReady === true", login="admin", timeout=45*60)


@incore.tests.tagged('click_all', 'post_install', '-at_install', '-standard')
class TestMenusDemo(incore.tests.HttpCase):

    def test_01_click_everywhere_as_demo(self):
        self.browser_js("/web", "incore.__DEBUG__.services['web.clickEverywhere']();", "incore.isReady === true", login="demo", timeout=1800)
