incore.define('mai_pos_kitchen_receipt.OrderKitchenReceipt', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');

	class OrderKitchenReceipt extends PosComponent {
		constructor() {
			super(...arguments);
			this._receiptEnv = this.props.order.getOrderReceiptEnv();
		}
		willUpdateProps(nextProps) {
			this._receiptEnv = nextProps.order.getOrderReceiptEnv();
		}
		get currentDate() {
			let today = new Date();
			let date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
			return date;
		}
		get currentTime() {
			let today = new Date();
			let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
			return time;
		}
		get order() {
			return this.receiptEnv.order;
		}
		get receipt() {
			return this.receiptEnv.receipt;
		}
		get orderlines() {
			return this.receiptEnv.orderlines;
		}
		get paymentlines() {
			return this.receiptEnv.paymentlines;
		}
		get isTaxIncluded() {
			return Math.abs(this.receipt.subtotal - this.receipt.total_with_tax) <= 0.000001;
		}
		get receiptEnv () {
		  return this._receiptEnv;
		}
	}
	OrderKitchenReceipt.template = 'OrderKitchenReceipt';

	Registries.Component.add(OrderKitchenReceipt);

	return OrderKitchenReceipt;
});
