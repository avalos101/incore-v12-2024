# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from functools import partial

import psycopg2

from incore import api, fields, models, tools, _
from incore.tools import float_is_zero
from incore.exceptions import UserError
from incore.http import request
import incore.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class PosConfig(models.Model):
    _inherit = 'pos.config' 

    allow_multi_uom = fields.Boolean('Product multi uom', default=True)

class ProductMultiUom(models.Model):
    _name = 'product.multi.uom'
    _order = "sequence desc"

    multi_uom_id = fields.Many2one('uom.uom','Unit of measure')
    price = fields.Float("Sale Price",default=0)
    sequence = fields.Integer("Sequence",default=1)
    barcode = fields.Char("Barcode")
    product_tmp_id = fields.Many2one("product.template",string="Product")
    product_id = fields.Many2one("product.product",string="Product")

    # @api.depends('product_tmp_id')
    # def _compute_product_tmp_id(self):
    #     for record in self:
    #         if record.product_tmp_id:
    #             record.product_id = record.product_tmp_id.product_tmp_id.ids[0]

    # @api.multi
    @api.onchange('multi_uom_id')
    def unit_id_change(self):
        domain = {'multi_uom_id': [('category_id', '=', self.product_tmp_id.uom_id.category_id.id)]}        
        return {'domain': domain}

    @api.model
    def create(self, vals):
        if 'barcode' in vals:
            barcodes = self.env['product.product'].sudo().search([('barcode','=',vals['barcode'])])
            barcodes2 = self.search([('barcode','=',vals['barcode'])])
            if barcodes or barcodes2:
                raise UserError(_('A barcode can only be assigned to one product !'))
        return super(ProductMultiUom, self).create(vals)

    # @api.multi
    def write(self, vals):
        if 'barcode' in vals:
            barcodes = self.env['product.product'].sudo().search([('barcode','=',vals['barcode'])])
            barcodes2 = self.search([('barcode','=',vals['barcode'])])
            if barcodes or barcodes2:
                raise UserError(_('A barcode can only be assigned to one product !'))
        return super(ProductMultiUom, self).write(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    has_multi_uom = fields.Boolean('Has multi UOM')
    multi_uom_ids = fields.One2many('product.multi.uom','product_tmp_id')

    @api.model
    def create(self, vals):
        if 'barcode' in vals:
            barcodes = self.env['product.multi.uom'].search([('barcode','=',vals['barcode'])])
            if barcodes:
                raise UserError(_('A barcode can only be assigned to one product !'))
        return super(ProductTemplate, self).create(vals)

    # @api.multi
    def write(self, vals):
        if 'barcode' in vals:
            barcodes = self.env['product.multi.uom'].search([('barcode','=',vals['barcode'])])
            if barcodes:
                raise UserError(_('A barcode can only be assigned to one product !'))
        return super(ProductTemplate, self).write(vals)

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    product_uom = fields.Many2one('uom.uom','Unit of measure')

class PosOrder(models.Model):
    _inherit = "pos.order"

    def create_picking(self):
        """Create a picking for each order and validate it."""
        Picking = self.env['stock.picking']
        Move = self.env['stock.move']
        StockWarehouse = self.env['stock.warehouse']
        for order in self:
            address = order.partner_id.address_get(['delivery']) or {}
            picking_type = order.picking_type_id
            return_pick_type = order.picking_type_id.return_picking_type_id or order.picking_type_id
            order_picking = Picking
            return_picking = Picking
            moves = Move
            location_id = order.location_id.id
            if order.partner_id:
                destination_id = order.partner_id.property_stock_customer.id
            else:
                if (not picking_type) or (not picking_type.default_location_dest_id):
                    customerloc, supplierloc = StockWarehouse._get_partner_locations()
                    destination_id = customerloc.id
                else:
                    destination_id = picking_type.default_location_dest_id.id

            if picking_type:
                message = _("This transfer has been created from the point of sale session: <a href=# data-oe-model=pos.order data-oe-id=%d>%s</a>") % (order.id, order.name)
                picking_vals = {
                    'origin': order.name,
                    'partner_id': address.get('delivery', False),
                    'date_done': order.date_order,
                    'picking_type_id': picking_type.id,
                    'company_id': order.company_id.id,
                    'move_type': 'direct',
                    'note': order.note or "",
                    'location_id': location_id,
                    'location_dest_id': destination_id,
                }
                pos_qty = any([x.qty >= 0 for x in order.lines])
                if pos_qty:
                    order_picking = Picking.create(picking_vals.copy())
                    order_picking.message_post(body=message)
                neg_qty = any([x.qty < 0 for x in order.lines])
                if neg_qty:
                    return_vals = picking_vals.copy()
                    return_vals.update({
                        'location_id': destination_id,
                        'location_dest_id': return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                        'picking_type_id': return_pick_type.id
                    })
                    return_picking = Picking.create(return_vals)
                    return_picking.message_post(body=message)

            for line in order.lines.filtered(lambda l: l.product_id.type in ['product', 'consu']):
                moves |= Move.create({
                    'name': line.name,
                    'product_uom': line.product_uom.id or line.product_id.uom_id.id,
                    'picking_id': order_picking.id if line.qty >= 0 else return_picking.id,
                    'picking_type_id': picking_type.id if line.qty >= 0 else return_pick_type.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': abs(line.qty),
                    'state': 'draft',
                    'location_id': location_id if line.qty >= 0 else destination_id,
                    'location_dest_id': destination_id if line.qty >= 0 else return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                })
            # prefer associating the regular order picking, not the return
            order.write({'picking_id': order_picking.id or return_picking.id})

            if return_picking:
                order._force_picking_done(return_picking)
            if order_picking:
                order._force_picking_done(order_picking)

            # when the pos.config has no picking_type_id set only the moves will be created
            if moves and not return_picking and not order_picking:
                moves.action_confirm()
                moves.force_assign()
                moves.filtered(lambda m: m.product_id.tracking == 'none').action_done()

        return True
    



