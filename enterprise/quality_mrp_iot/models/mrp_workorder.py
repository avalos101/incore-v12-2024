# -*- encoding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import fields, models, _
from incore.exceptions import UserError
import json


class MrpProductionWorkcenterLine(models.Model):
    _inherit = "mrp.workorder"

    ip = fields.Char(related='current_quality_check_id.point_id.device_id.iot_id.ip')
    identifier = fields.Char(related='current_quality_check_id.point_id.device_id.identifier')
    boxes = fields.Char(compute='_compute_boxes')
    device_name = fields.Char(related='current_quality_check_id.point_id.device_id.name', size=30, string='Device Name: ')

    def _compute_boxes(self):
        for wo in self:
            triggers = wo.workcenter_id.trigger_ids
            box_dict = {}
            for trigger in triggers:
                box = trigger.device_id.iot_id.ip
                box_dict.setdefault(box, [])
                box_dict[box].append([trigger.device_id.identifier, trigger.key, trigger.action])
            wo.boxes = json.dumps(box_dict)


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    trigger_ids = fields.One2many('iot.trigger', 'workcenter_id', string="Triggers")


class IotTrigger(models.Model):
    _inherit = 'iot.trigger'

    workcenter_id = fields.Many2one('mrp.workcenter')
