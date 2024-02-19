# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import models


class QualityPoint(models.Model):
    _inherit = "quality.point"

    def check_execute_now(self):
        if self.test_type == 'print_label':
            return True
        else:
            return super(QualityPoint, self).check_execute_now()
