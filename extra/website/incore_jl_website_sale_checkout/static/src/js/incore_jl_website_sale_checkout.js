incore.define("incore_jl_website_sale_checkout.CheckoutAdditionalFields", function(require){
    "use strict";

    var sAnimations = require('website.content.snippets.animation');

    sAnimations.registry.CheckoutAdditionalFields = sAnimations.Class.extend({
	selector: '.oe_website_sale .oe_cart .form-row',
	read_events: {
	    "click .js-order-gift": "_onClickGift",
	    "change #xidentification": "_onChangeXidentification",
	    "change #doctype": "_onChangeDoctype",
	},

	/**
	 * @private
	 * @param {Event} ev
	 */
	_onClickGift: function (ev) {
	    var giftTextareaSelector = this.selector + " .js-order-gift-msg";
	    if ($(giftTextareaSelector).css("display") == "none"){
		$(giftTextareaSelector).css("display", "block");
	    }
	    else {
		$(giftTextareaSelector).css("display", "none");
	    }
	},

	/**
	 * @private
	 * @param {Event} ev
	 */
	_onChangeXidentification: function (ev) {
	    var xidentificationInput = $("#xidentification");
	    var doctypeSelect = $("#doctype");

	    if (xidentificationInput.val() != "" && doctypeSelect.val() == "31"){
		this._rpc({
		    route: "/shop/checkout/get_nit_formatted",
		    params: {
			xidentification: xidentificationInput.val(),
		    },
		}).then(function (data){

		    var formattedNitInput = $("#formatedNit");
		    if (data.nit_formatted){
			var formattedNitInputVisible = false;

			if ( formattedNitInput.css("display") != "none" ){
			    formattedNitInputVisible = true;
			}

			if (!formattedNitInputVisible) {
			    formattedNitInput.css("display", "block");
			    var labelNitInput = $("label[for='formatedNit']");
			    labelNitInput.css("display", "block");
			}

			formattedNitInput.val(data.nit_formatted);
		    }
		    else {
			formattedNitInput.val("");
		    }

		});
	    }
	},

	/**
	 * @private
	 * @param {Event} ev
	 */
	_onChangeDoctype: function( ev ) {
	    var doctypeSelect = $("#doctype");
	    if (doctypeSelect.val() != "31"){
		var formattedNitInput = $("#formatedNit");
		var formattedNitInputVisible = false;

		if ( formattedNitInput.css("display") != "none" ){
		    formattedNitInputVisible = true;
		}

		if (formattedNitInputVisible){
		    formattedNitInput.css("display", "none");
		    var labelNitInput = $("label[for='formatedNit']");
		    labelNitInput.css("display", "none");
		}
	    }
	    else {
		this._onChangeXidentification();
	    }
	},
    });
});
