incore.define("mai_pos_kitchen_receipt.models", function (require) {
"use strict";

    // var screens = require('point_of_sale.screens');
    // var core = require('web.core');
    // var rpc = require('web.rpc');
    // var gui = require('point_of_sale.gui');
    // var QWeb = core.qweb;

	var models = require('point_of_sale.models');

	models.load_fields('res.company', ['street','street2','city','zip']);

    // screens.define_action_button({
    //     'name': 'Kitchen Report',
    //     'widget': KitchenReceiptButton,
    //     'condition': function(){
    //         return this.pos.config.print_kitchen_receipt;
    //     },
    // });

})