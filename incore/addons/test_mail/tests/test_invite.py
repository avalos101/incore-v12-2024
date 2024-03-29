# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore.addons.test_mail.tests import common
from incore.tools import mute_logger


class TestInvite(common.BaseFunctionalTest, common.MockEmails):

    @mute_logger('incore.addons.mail.models.mail_mail')
    def test_invite_email(self):
        test_partner = self.env['res.partner'].with_context(common.BaseFunctionalTest._test_context).create({
            'name': 'Valid Lelitre',
            'email': 'valid.lelitre@agrolait.com'})

        mail_invite = self.env['mail.wizard.invite'].with_context({
            'default_res_model': 'mail.test.simple',
            'default_res_id': self.test_record.id
        }).sudo(self.user_employee.id).create({
            'partner_ids': [(4, test_partner.id), (4, self.user_admin.partner_id.id)],
            'send_mail': True})
        mail_invite.add_followers()

        # check added followers and that emails were sent
        self.assertEqual(self.test_record.message_partner_ids,
                         test_partner | self.user_admin.partner_id)
        self.assertEqual(self.test_record.message_follower_ids.mapped('channel_id'),
                         self.env['mail.channel'])
        self.assertEqual(len(self._mails), 2)
