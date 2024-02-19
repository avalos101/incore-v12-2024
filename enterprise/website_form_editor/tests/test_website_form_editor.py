# Part of inCore. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-

import incore.tests


@incore.tests.tagged('post_install','-at_install')
class TestWebsiteFormEditor(incore.tests.HttpCase):
    def test_tour(self):
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('website_form_editor_tour')", "incore.__DEBUG__.services['web_tour.tour'].tours.website_form_editor_tour.ready", login="admin")
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('website_form_editor_tour_submit')", "incore.__DEBUG__.services['web_tour.tour'].tours.website_form_editor_tour_submit.ready")
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('website_form_editor_tour_results')", "incore.__DEBUG__.services['web_tour.tour'].tours.website_form_editor_tour_results.ready", login="admin")
