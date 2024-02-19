# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore.api import Environment
import incore.tests

@incore.tests.tagged('post_install', '-at_install')
class TestWebsiteHrRecruitmentForm(incore.tests.HttpCase):
    def test_tour(self):
        self.phantom_js("/", "incore.__DEBUG__.services['web_tour.tour'].run('website_hr_recruitment_tour')", "incore.__DEBUG__.services['web_tour.tour'].tours.website_hr_recruitment_tour.ready")

        # check result
        record = self.env['hr.applicant'].search([('description', '=', '### HR RECRUITMENT TEST DATA ###')])
        self.assertEqual(len(record), 1)
        self.assertEqual(record.partner_name, "John Smith")
        self.assertEqual(record.email_from, "john@smith.com")
        self.assertEqual(record.partner_phone, '118.218')
