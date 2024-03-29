# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.
import unittest
from incore.addons.stock_landed_costs.tests.common import TestStockLandedCostsCommon
from incore.tests import tagged


@tagged('post_install', '-at_install')
class TestLandedCosts(TestStockLandedCostsCommon):

    def setUp(self):
        super(TestLandedCosts, self).setUp()
        # Create picking incoming shipment
        self.picking_in = self.Picking.create({
            'partner_id': self.supplier_id,
            'picking_type_id': self.picking_type_in_id,
            'location_id': self.supplier_location_id,
            'location_dest_id': self.stock_location_id})
        self.Move.create({
            'name': self.product_refrigerator.name,
            'product_id': self.product_refrigerator.id,
            'product_uom_qty': 5,
            'product_uom': self.product_refrigerator.uom_id.id,
            'picking_id': self.picking_in.id,
            'location_id': self.supplier_location_id,
            'location_dest_id': self.stock_location_id})
        self.Move.create({
            'name': self.product_oven.name,
            'product_id': self.product_oven.id,
            'product_uom_qty': 10,
            'product_uom': self.product_oven.uom_id.id,
            'picking_id': self.picking_in.id,
            'location_id': self.supplier_location_id,
            'location_dest_id': self.stock_location_id})
        # Create picking outgoing shipment
        self.picking_out = self.Picking.create({
            'partner_id': self.customer_id,
            'picking_type_id': self.picking_type_out_id,
            'location_id': self.stock_location_id,
            'location_dest_id': self.customer_location_id})
        self.Move.create({
            'name': self.product_refrigerator.name,
            'product_id': self.product_refrigerator.id,
            'product_uom_qty': 2,
            'product_uom': self.product_refrigerator.uom_id.id,
            'picking_id': self.picking_out.id,
            'location_id': self.stock_location_id,
            'location_dest_id': self.customer_location_id})

    def test_00_landed_costs_on_incoming_shipment(self):
        chart_of_accounts = self.env.user.company_id.chart_template_id
        generic_coa = self.env.ref('l10n_generic_coa.configurable_chart_template')
        if chart_of_accounts != generic_coa:
            raise unittest.SkipTest('Skip this test as it works only with %s (%s loaded)' % (generic_coa.name, chart_of_accounts.name))
        """ Test landed cost on incoming shipment """
        #
        # (A) Purchase product

        #         Services           Quantity       Weight      Volume
        #         -----------------------------------------------------
        #         1. Refrigerator         5            10          1
        #         2. Oven                 10           20          1.5

        # (B) Add some costs on purchase

        #         Services           Amount     Split Method
        #         -------------------------------------------
        #         1.labour            10        By Equal
        #         2.brokerage         150       By Quantity
        #         3.transportation    250       By Weight
        #         4.packaging         20        By Volume

        # Process incoming shipment
        income_ship = self._process_incoming_shipment()
        # Create landed costs
        stock_landed_cost = self._create_landed_costs({
            'equal_price_unit': 10,
            'quantity_price_unit': 150,
            'weight_price_unit': 250,
            'volume_price_unit': 20}, income_ship)
        # Compute landed costs
        stock_landed_cost.compute_landed_cost()

        valid_vals = {
            'equal': 5.0,
            'by_quantity_refrigerator': 50.0,
            'by_quantity_oven': 100.0,
            'by_weight_refrigerator': 50.0,
            'by_weight_oven': 200,
            'by_volume_refrigerator': 5.0,
            'by_volume_oven': 15.0}

        # Check valuation adjustment line recognized or not
        self._validate_additional_landed_cost_lines(stock_landed_cost, valid_vals)
        # Validate the landed cost.
        stock_landed_cost.button_validate()
        self.assertTrue(stock_landed_cost.account_move_id, 'Landed costs should be available account move lines')
        account_entry = self.env['account.move.line'].read_group(
            [('move_id', '=', stock_landed_cost.account_move_id.id)], ['debit', 'credit', 'move_id'], ['move_id'])[0]
        self.assertEqual(account_entry['debit'], account_entry['credit'], 'Debit and credit are not equal')
        self.assertEqual(account_entry['debit'], 430.0, 'Wrong Account Entry')

    def test_01_negative_landed_costs_on_incoming_shipment(self):
        chart_of_accounts = self.env.user.company_id.chart_template_id
        generic_coa = self.env.ref('l10n_generic_coa.configurable_chart_template')
        if chart_of_accounts != generic_coa:
            raise unittest.SkipTest('Skip this test as it works only with %s (%s loaded)' % (generic_coa.name, chart_of_accounts.name))

        """ Test negative landed cost on incoming shipment """
        #
        # (A) Purchase Product

        #         Services           Quantity       Weight      Volume
        #         -----------------------------------------------------
        #         1. Refrigerator         5            10          1
        #         2. Oven                 10           20          1.5

        # (B) Sale refrigerator's part of the quantity

        # (C) Add some costs on purchase

        #         Services           Amount     Split Method
        #         -------------------------------------------
        #         1.labour            10        By Equal
        #         2.brokerage         150       By Quantity
        #         3.transportation    250       By Weight
        #         4.packaging         20        By Volume

        # (D) Decrease cost that already added on purchase
        #         (apply negative entry)

        #         Services           Amount     Split Method
        #         -------------------------------------------
        #         1.labour            -5        By Equal
        #         2.brokerage         -50       By Quantity
        #         3.transportation    -50       By Weight
        #         4.packaging         -5        By Volume

        # Process incoming shipment
        income_ship = self._process_incoming_shipment()
        # Refrigerator outgoing shipment.
        self._process_outgoing_shipment()
        # Apply landed cost for incoming shipment.
        stock_landed_cost = self._create_landed_costs({
            'equal_price_unit': 10,
            'quantity_price_unit': 150,
            'weight_price_unit': 250,
            'volume_price_unit': 20}, income_ship)
        # Compute landed costs
        stock_landed_cost.compute_landed_cost()
        valid_vals = {
            'equal': 5.0,
            'by_quantity_refrigerator': 50.0,
            'by_quantity_oven': 100.0,
            'by_weight_refrigerator': 50.0,
            'by_weight_oven': 200.0,
            'by_volume_refrigerator': 5.0,
            'by_volume_oven': 15.0}
        # Check valuation adjustment line recognized or not
        self._validate_additional_landed_cost_lines(stock_landed_cost, valid_vals)
        # Validate the landed cost.
        stock_landed_cost.button_validate()
        self.assertTrue(stock_landed_cost.account_move_id, 'Landed costs should be available account move lines')
        # Create negative landed cost for previously incoming shipment.
        stock_negative_landed_cost = self._create_landed_costs({
            'equal_price_unit': -5,
            'quantity_price_unit': -50,
            'weight_price_unit': -50,
            'volume_price_unit': -5}, income_ship)
        # Compute negative landed costs
        stock_negative_landed_cost.compute_landed_cost()
        valid_vals = {
            'equal': -2.5,
            'by_quantity_refrigerator': -16.67,
            'by_quantity_oven': -33.33,
            'by_weight_refrigerator': -10.00,
            'by_weight_oven': -40.00,
            'by_volume_refrigerator': -1.25,
            'by_volume_oven': -3.75}
        # Check valuation adjustment line recognized or not
        self._validate_additional_landed_cost_lines(stock_negative_landed_cost, valid_vals)
        # Validate the landed cost.
        stock_negative_landed_cost.button_validate()
        self.assertEqual(stock_negative_landed_cost.state, 'done', 'Negative landed costs should be in done state')
        self.assertTrue(stock_negative_landed_cost.account_move_id, 'Landed costs should be available account move lines')
        account_entry = self.env['account.move.line'].read_group(
            [('move_id', '=', stock_negative_landed_cost.account_move_id.id)], ['debit', 'credit', 'move_id'], ['move_id'])[0]
        self.assertEqual(account_entry['debit'], account_entry['credit'], 'Debit and credit are not equal')
        move_lines = [
            {'name': 'split by volume - Microwave Oven',                    'debit': 3.75,  'credit': 0.0},
            {'name': 'split by volume - Microwave Oven',                    'debit': 0.0,   'credit': 3.75},
            {'name': 'split by weight - Microwave Oven',                    'debit': 40.0,  'credit': 0.0},
            {'name': 'split by weight - Microwave Oven',                    'debit': 0.0,   'credit': 40.0},
            {'name': 'split by quantity - Microwave Oven',                  'debit': 33.33, 'credit': 0.0},
            {'name': 'split by quantity - Microwave Oven',                  'debit': 0.0,   'credit': 33.33},
            {'name': 'equal split - Microwave Oven',                        'debit': 2.5,   'credit': 0.0},
            {'name': 'equal split - Microwave Oven',                        'debit': 0.0,   'credit': 2.5},
            {'name': 'split by volume - Refrigerator: 2.0 already out',     'debit': 0.5,   'credit': 0.0},
            {'name': 'split by volume - Refrigerator: 2.0 already out',     'debit': 0.0,   'credit': 0.5},
            {'name': 'split by weight - Refrigerator: 2.0 already out',     'debit': 4.0,   'credit': 0.0},
            {'name': 'split by weight - Refrigerator: 2.0 already out',     'debit': 0.0,   'credit': 4.0},
            {'name': 'split by weight - Refrigerator',                      'debit': 0.0,   'credit': 10.0},
            {'name': 'split by weight - Refrigerator',                      'debit': 10.0,  'credit': 0.0},
            {'name': 'split by volume - Refrigerator',                      'debit': 0.0,   'credit': 1.25},
            {'name': 'split by volume - Refrigerator',                      'debit': 1.25,  'credit': 0.0},
            {'name': 'split by quantity - Refrigerator: 2.0 already out',   'debit': 6.67,  'credit': 0.0},
            {'name': 'split by quantity - Refrigerator: 2.0 already out',   'debit': 0.0,   'credit': 6.67},
            {'name': 'split by quantity - Refrigerator',                    'debit': 16.67, 'credit': 0.0},
            {'name': 'split by quantity - Refrigerator',                    'debit': 0.0,   'credit': 16.67},
            {'name': 'equal split - Refrigerator: 2.0 already out',         'debit': 1.0,   'credit': 0.0},
            {'name': 'equal split - Refrigerator: 2.0 already out',         'debit': 0.0,   'credit': 1.0},
            {'name': 'equal split - Refrigerator',                          'debit': 2.5,   'credit': 0.0},
            {'name': 'equal split - Refrigerator',                          'debit': 0.0,   'credit': 2.5}
        ]
        if stock_negative_landed_cost.account_move_id.company_id.anglo_saxon_accounting:
            move_lines += [
                {'name': 'split by volume - Refrigerator: 2.0 already out',     'debit': 0.5,   'credit': 0.0},
                {'name': 'split by volume - Refrigerator: 2.0 already out',     'debit': 0.0,   'credit': 0.5},
                {'name': 'split by weight - Refrigerator: 2.0 already out',     'debit': 4.0,   'credit': 0.0},
                {'name': 'split by weight - Refrigerator: 2.0 already out',     'debit': 0.0,   'credit': 4.0},
                {'name': 'split by quantity - Refrigerator: 2.0 already out',   'debit': 6.67,  'credit': 0.0},
                {'name': 'split by quantity - Refrigerator: 2.0 already out',   'debit': 0.0,   'credit': 6.67},
                {'name': 'equal split - Refrigerator: 2.0 already out',         'debit': 1.0,   'credit': 0.0},
                {'name': 'equal split - Refrigerator: 2.0 already out',         'debit': 0.0,   'credit': 1.0},
            ]
        self.assertRecordValues(
            sorted(stock_negative_landed_cost.account_move_id.line_ids, key=lambda d: (d['name'], d['debit'])),
            sorted(move_lines, key=lambda d: (d['name'], d['debit'])),
        )

    def _process_incoming_shipment(self):
        """ Two product incoming shipment. """
        # Confirm incoming shipment.
        self.picking_in.action_confirm()
        # Transfer incoming shipment
        res_dict = self.picking_in.button_validate()
        wizard = self.env[(res_dict.get('res_model'))].browse(res_dict.get('res_id'))
        wizard.process()
        return self.picking_in

    def _process_outgoing_shipment(self):
        """ One product Outgoing shipment. """
        # Confirm outgoing shipment.
        self.picking_out.action_confirm()
        # Product assign to outgoing shipments
        self.picking_out.action_assign()
        # Transfer picking.

        res_dict = self.picking_out.button_validate()
        wizard = self.env[(res_dict.get('res_model'))].browse(res_dict.get('res_id'))
        wizard.process()

    def _create_landed_costs(self, value, picking_in):
        return self.LandedCost.create(dict(
            picking_ids=[(6, 0, [picking_in.id])],
            account_journal_id=self.expenses_journal.id,
            cost_lines=[
                (0, 0, {
                    'name': 'equal split',
                    'split_method': 'equal',
                    'price_unit': value['equal_price_unit'],
                    'product_id': self.landed_cost.id}),
                (0, 0, {
                    'name': 'split by quantity',
                    'split_method': 'by_quantity',
                    'price_unit': value['quantity_price_unit'],
                    'product_id': self.brokerage_quantity.id}),
                (0, 0, {
                    'name': 'split by weight',
                    'split_method': 'by_weight',
                    'price_unit': value['weight_price_unit'],
                    'product_id': self.transportation_weight.id}),
                (0, 0, {
                    'name': 'split by volume',
                    'split_method': 'by_volume',
                    'price_unit': value['volume_price_unit'],
                    'product_id': self.packaging_volume.id})
            ],
        ))

    def _validate_additional_landed_cost_lines(self, stock_landed_cost, valid_vals):
        for valuation in stock_landed_cost.valuation_adjustment_lines:
            add_cost = valuation.additional_landed_cost
            split_method = valuation.cost_line_id.split_method
            product = valuation.move_id.product_id
            if split_method == 'equal':
                self.assertEqual(add_cost, valid_vals['equal'], self._error_message(valid_vals['equal'], add_cost))
            elif split_method == 'by_quantity' and product == self.product_refrigerator:
                self.assertEqual(add_cost, valid_vals['by_quantity_refrigerator'], self._error_message(valid_vals['by_quantity_refrigerator'], add_cost))
            elif split_method == 'by_quantity' and product == self.product_oven:
                self.assertEqual(add_cost, valid_vals['by_quantity_oven'], self._error_message(valid_vals['by_quantity_oven'], add_cost))
            elif split_method == 'by_weight' and product == self.product_refrigerator:
                self.assertEqual(add_cost, valid_vals['by_weight_refrigerator'], self._error_message(valid_vals['by_weight_refrigerator'], add_cost))
            elif split_method == 'by_weight' and product == self.product_oven:
                self.assertEqual(add_cost, valid_vals['by_weight_oven'], self._error_message(valid_vals['by_weight_oven'], add_cost))
            elif split_method == 'by_volume' and product == self.product_refrigerator:
                self.assertEqual(add_cost, valid_vals['by_volume_refrigerator'], self._error_message(valid_vals['by_volume_refrigerator'], add_cost))
            elif split_method == 'by_volume' and product == self.product_oven:
                self.assertEqual(add_cost, valid_vals['by_volume_oven'], self._error_message(valid_vals['by_volume_oven'], add_cost))

    def _error_message(self, actucal_cost, computed_cost):
        return 'Additional Landed Cost should be %s instead of %s' % (actucal_cost, computed_cost)
