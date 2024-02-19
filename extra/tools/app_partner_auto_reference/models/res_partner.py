# -*- coding: utf-8 -*-

import uuid
from incore import api, fields, models, _
from incore.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"
    _order = "sequence, display_name"

    sequence = fields.Integer('Sequence', default=20, help="Determine the display order. Sort ascending.")

    @api.multi
    def _needsRef(self, vals=None):
        """
        可调整的逻辑
        单独建的partner，员工类型的，要加 ref
        公司下面的联系人，不要ref
        """
        if not vals and not self:  # pragma: no cover
            raise UserError(_(
                'Either field values or an id must be provided.'))
        # only assign a 'ref' to commercial partners
        if self:
            vals = {}
            vals['is_company'] = self.is_company
            vals['parent_id'] = self.parent_id

        res = (vals.get('is_company') and vals['is_company']) or not vals.get('parent_id') or vals.get('employee')
        return res

    # todo: 检查数据，要保证数据唯一性，使用api便于逻辑变更时调整
    @api.constrains('ref')
    def _check_ref(self):
        if self.ref:
            customers = self.search([('ref', '=', self.ref)], limit=2)
            if len(customers) > 1:
                raise ValidationError(_('The reference must be unique! Try save again.'))

    @api.depends('ref', 'is_company', 'name', 'parent_id.name', 'type', 'company_name')
    def _compute_display_name(self):
        super(ResPartner, self)._compute_display_name()

    # 如果有 show_ref 才显示ref
    @api.multi
    def name_get(self):
        res = []
        for partner in self:
            name = partner._get_name()
            if partner.ref and self._context.get('show_ref'):
                name = "[" + partner.ref + "]" + name
            res.append((partner.id, name))
        return res

    @api.multi
    def _get_next_ref(self, vals=None):
        ref = ''
        if (not vals.get('ref') or vals['ref'] is False or vals['ref'] == _('New')) and self._needsRef(vals=vals):
            if 'customer' in vals and vals['customer']:
                try:
                    sequence = self.env.ref('app_partner_auto_reference.seq_res_partner_customer', raise_if_not_found=False)
                except:
                    sequence = False
            elif 'supplier' in vals and vals['supplier']:
                try:
                    sequence = self.env.ref('app_partner_auto_reference.seq_res_partner_supplier', raise_if_not_found=False)
                except:
                    sequence = False
            elif 'emplyoee' in vals and vals['emplyoee']:
                try:
                    sequence = self.env.ref('app_partner_auto_reference.seq_res_partner_employee', raise_if_not_found=False)
                except:
                    sequence = False
            else:
                sequence = self.env.ref('app_partner_auto_reference.seq_res_partner_default', raise_if_not_found=False)

            if sequence:
                ref = sequence.next_by_id()
            else:
                # 没有则用 uuid
                ref = str(uuid.uuid1())

        return ref

    @api.model
    def create(self, vals):
        """
        默认用户编码
        """
        vals['ref'] = self._get_next_ref(vals=vals)
        if vals['ref']:
            vals['barcode'] = vals['ref']
                
        return super(ResPartner, self).create(vals)

    @api.multi
    def copy(self, default=None):
        # copy 时不要有 ref
        default = default or {}
        if self._needsRef():
            default['ref'] = self._get_next_ref()
        return super(ResPartner, self).copy(default)

    @api.multi
    def write(self, vals):
        for partner in self:
            if not vals.get('ref') and partner._needsRef(vals) and \
                    not partner.ref:
                vals['ref'] = partner._get_next_ref(vals=vals)
            super(ResPartner, partner).write(vals)
        return True

