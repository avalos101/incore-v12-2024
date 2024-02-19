incore.define('mai_pos_kitchen_receipt.KitchenReceiptButton', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const ProductScreen = require('point_of_sale.ProductScreen');
	const { useListener } = require('web.custom_hooks');
	const Registries = require('point_of_sale.Registries');

	class KitchenReceiptButton extends PosComponent {
		constructor() {
			super(...arguments);
			useListener('click', this.onClick);
		}
		async onClick() {
			const order = this.env.pos.get_order();
			if (order.get_orderlines().length > 0) {
				await this.showTempScreen('CustomKitchenScreen');
			} else {
				await this.showPopup('ErrorPopup', {
					title: this.env._t('Nothing to Print'),
					body: this.env._t('There are no order lines'),
				});
			}
		}
	}
	KitchenReceiptButton.template = 'KitchenReceiptButton';

	ProductScreen.addControlButton({
		component: KitchenReceiptButton,
		condition: function() {
			return this.env.pos.config.print_kitchen_receipt;
		},
	});

	Registries.Component.add(KitchenReceiptButton);

	return KitchenReceiptButton;
});
