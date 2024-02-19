# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_mass_mailing_campaign = fields.Boolean(string="Mass Mailing Campaigns", implied_group='mass_mailing.group_mass_mailing_campaign', help="""This is useful if your marketing campaigns are composed of several emails""")
    mass_mailing_outgoing_mail_server = fields.Boolean(string="Specific Mail Server", config_parameter='mass_mailing.outgoing_mail_server',
        help='Use a specific mail server in priority. Otherwise inCore relies on the first outgoing mail server available (based on their sequencing) as it does for normal mails.')
    mass_mailing_mail_server_id = fields.Many2one('ir.mail_server', string='Mail Server', config_parameter='mass_mailing.mail_server_id')
    show_blacklist_buttons = fields.Boolean(string="Show blacklist buttons on unsubscribe page",
                                                 config_parameter='mass_mailing.show_blacklist_buttons',
                                                 help="""Allow the recipient to manage himself his state in the blacklist via the unsubscription page.""")

    @api.onchange('mass_mailing_outgoing_mail_server')
    def _onchange_mass_mailing_outgoing_mail_server(self):
        if not self.mass_mailing_outgoing_mail_server:
            self.mass_mailing_mail_server_id = False
