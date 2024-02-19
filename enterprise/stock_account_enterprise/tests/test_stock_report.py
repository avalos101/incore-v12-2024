# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from incore import fields
from incore.exceptions import UserError
from incore.tests import common


class TestStockReport(common.TransactionCase):
    def setUp(self):
        super(TestStockReport, self).setUp()

        products = self.env['product.product'].with_context(to_date=fields.Date.today()).search([('product_tmpl_id.type', '=', 'product')])
        moves = self.env['stock.move'].search([])
        incoming_moves = self.env['stock.move'].search([('picking_id.picking_type_id.code', '=', 'incoming')])

        self.inventory_valuation = sum(product.stock_value for product in products)
        self.total_move_valuation = sum(move.product_qty * move.product_id.standard_price for move in moves)
        self.incoming_move_valuation = sum(move.product_qty * move.product_id.standard_price for move in incoming_moves)

    def test_valuation(self):
        # without domain
        value = self.env['stock.report'].read_group([], ['valuation:sum(valuation)'], '')

        self.assertEqual(value[0]['valuation'], self.total_move_valuation,
                         "Calling read group with valuation and without domain should give the total move valuation of the inventory")

        # with domain
        value = self.env['stock.report'].read_group([('picking_type_code', '=', 'incoming')], ['valuation:sum(valuation)'], '')

        self.assertEqual(value[0]['valuation'], self.incoming_move_valuation,
                         "Calling read group with valuation and with domain should give the move valuation for this domain")

        # Doesn't support group by
        with self.assertRaises(UserError):
            value = self.env['stock.report'].read_group([('picking_type_code', '=', 'incoming')], ['valuation:sum(valuation)'], 'state')

        # Only support sum operator
        with self.assertRaises(UserError):
            value = self.env['stock.report'].read_group([('picking_type_code', '=', 'incoming')], ['valuation:avg(valuation)'], '')

    def test_stock_value(self):
        def get_test_date():
            return fields.Datetime.to_string(fields.Datetime.from_string(fields.Datetime.now()) - timedelta(days=5))

        # without domain
        value = self.env['stock.report'].read_group([], ['stock_value:sum(stock_value)'], '')

        self.assertEqual(value[0]['stock_value'], self.inventory_valuation,
                         "Calling read group with stock_value should give the total inventory value to this date")

        # Takes date_done into account when in domain but doesn't care about the operator
        value = self.env['stock.report'].read_group([('date_done', '=', get_test_date())], ['stock_value:sum(stock_value)'], '')

        self.assertEqual(value[0]['stock_value'], 0,
                         "Read group on stock_value should take date_done into account in domain")

        value = self.env['stock.report'].read_group([('date_done', '<', get_test_date())], ['stock_value:sum(stock_value)'], '')

        self.assertEqual(value[0]['stock_value'], 0,
                         "Read group on stock_value should take date_done into account in domain in the same manner whatever the operator is")

        # with domain should be the same value
        value = self.env['stock.report'].read_group([('picking_type_code', '=', 'incoming')], ['stock_value:sum(stock_value)'], '')

        self.assertEqual(value[0]['stock_value'], self.inventory_valuation,
                         "Read group on stock_value should ignore domain")

        # Doesn't support group by
        with self.assertRaises(UserError):
            value = self.env['stock.report'].read_group([], ['stock_value:sum(stock_value)'], 'state')

        # Only support sum operator
        with self.assertRaises(UserError):
            value = self.env['stock.report'].read_group([], ['stock_value:avg(stock_value)'], '')