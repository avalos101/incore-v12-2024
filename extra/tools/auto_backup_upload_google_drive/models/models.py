# -*- coding: utf-8 -*-

from incore import models, fields, api

# class auto_backup_upload(models.Model):
#     _name = 'auto_backup_upload.auto_backup_upload'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100