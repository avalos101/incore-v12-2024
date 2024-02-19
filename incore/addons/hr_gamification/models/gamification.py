# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from incore import api, fields, models, _
from incore.exceptions import ValidationError


class GamificationBadgeUser(models.Model):
    """User having received a badge"""
    _inherit = 'gamification.badge.user'

    employee_id = fields.Many2one('hr.employee', string='Employee')

    @api.constrains('employee_id')
    def _check_employee_related_user(self):
        for badge_user in self:
            if badge_user.employee_id not in badge_user.user_id.employee_ids:
                raise ValidationError(_('The selected employee does not correspond to the selected user.'))


class GamificationBadge(models.Model):
    _inherit = 'gamification.badge'

    granted_employees_count = fields.Integer(compute="_compute_granted_employees_count")

    @api.depends('owner_ids.employee_id')
    def _compute_granted_employees_count(self):
        for badge in self:
            badge.granted_employees_count = self.env['gamification.badge.user'].search_count([
                ('badge_id', '=', badge.id),
                ('employee_id', '!=', False)
            ])

    @api.multi
    def get_granted_employees(self):
        employee_ids = self.mapped('owner_ids.employee_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Granted Employees',
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'res_model': 'hr.employee',
            'domain': [('id', 'in', employee_ids)]
        }
