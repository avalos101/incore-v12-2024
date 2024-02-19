incore.define('mai_pos_kitchen_receipt.CustomKitchenScreen', function (require) {
	'use strict';

	const ReceiptScreen = require('point_of_sale.ReceiptScreen');
	const Registries = require('point_of_sale.Registries');

	const CustomKitchenScreen = (ReceiptScreen) => {
		class CustomKitchenScreen extends ReceiptScreen {
			confirm() {
				this.props.resolve({ confirmed: true, payload: null });
				this.trigger('close-temp-screen');
			}
		}
		CustomKitchenScreen.template = 'CustomKitchenScreen';
		return CustomKitchenScreen;
	};

	Registries.Component.addByExtending(CustomKitchenScreen, ReceiptScreen);

	return CustomKitchenScreen;
});
