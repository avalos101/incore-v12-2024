incore.define('website_sale_stock_available.ProductConfiguratorMixin', function (require) {
    'use strict';

    var ProductConfiguratorMixin = require('sale.ProductConfiguratorMixin');
    var sAnimations = require('website.content.snippets.animation');

    /**
     * Addition to the product_configurator_mixin._onChangeCombination
     *
     * This will show a message if varian is not available in stock.
     *
     * @param {MouseEvent} ev
     * @param {$.Element} $parent
     * @param {Array} combination
     */
    ProductConfiguratorMixin._onChangeCombinationStockAvailable = function (ev, $parent, combination) {
	if (combination.inventory_availability == 'never'){
	    var elem_msg = $parent.find("p.not_available_custom_msg");
	    if ((combination.virtual_available <= 0 && combination.product_template_virtual_available > 0) || (combination.product_variant_count == 1 && combination.product_template_virtual_available <= 0)){
		if (elem_msg.length){
		    elem_msg.css("display", "block");
		    elem_msg.text(combination.custom_message);
		}
	    }
	    else{
		if (elem_msg.length){
		    elem_msg.css("display", "none");
		}
	    }
	}
    };    

    sAnimations.registry.WebsiteSale.include({
	/**
	 * Adds the stock availability checking to the regular _onChangeCombination method
	 * @override
	 */
	_onChangeCombination: function (){
            this._super.apply(this, arguments);
            ProductConfiguratorMixin._onChangeCombinationStockAvailable.apply(this, arguments);
	}
    });    

    return ProductConfiguratorMixin;
});
