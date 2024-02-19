# -*- coding: utf-8 -*-

from incore import models
from incore.tools.translate import _
from incore.tools.misc import formatLang, format_date

LINE_FILLER = '*'

class report_print_check(models.Model):
    _inherit = 'account.payment'

