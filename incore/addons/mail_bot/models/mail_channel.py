# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import api, models, _


class Channel(models.Model):
    _inherit = 'mail.channel'

    def _execute_command_help(self, **kwargs):
        super(Channel, self)._execute_command_help(**kwargs)
        self.env['mail.bot']._apply_logic(self, kwargs, command="help")  # kwargs are not usefull but...

    @api.model
    def init_incorebot(self):
        if self.env.user.incorebot_state == 'not_initialized':
            partner = self.env.user.partner_id
            incorebot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
            channel = self.with_context({"mail_create_nosubscribe": True}).create({
                'channel_partner_ids': [(4, partner.id), (4, incorebot_id)],
                'public': 'private',
                'channel_type': 'chat',
                'email_send': False,
                'name': 'inCoreBot'
            })
            message = _("Hello,<br/>inCore's chat helps employees collaborate efficiently. I'm here to help you discover its features.<br/><b>Try to send me an emoji :)</b>")
            channel.sudo().message_post(body=message, author_id=incorebot_id, message_type="comment", subtype="mail.mt_comment")
            self.env.user.incorebot_state = 'onboarding_emoji'
            return channel
