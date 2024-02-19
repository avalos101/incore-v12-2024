# Copyright 2018  <https://incore.co/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from incore import models, fields


class Journal(models.Model):
    _inherit = 'account.journal'

    wechat = fields.Selection([
        ('micropay', 'Scanning customer\'s QR'),
        ('native', 'Showing QR to customer'),
    ], string='WeChat Payment', help='Register for WeChat payment')
