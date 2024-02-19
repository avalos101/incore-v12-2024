incore.define('incore_jl_website_signup.signup', function (require) {
    'use strict';

    var base = require('web_editor.base');

    var sAnimations = require('website.content.snippets.animation');
    
    sAnimations.registry.IncoreSignup = sAnimations.Class.extend({
	selector: '.oe_signup_form',
	read_events: {
	    "change #xidentification": "_onChangeXidentification",
	    "change #doctype": "_onChangeDoctype",
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
