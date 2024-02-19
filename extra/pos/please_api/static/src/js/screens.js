incore.define('l10n_pe_pos.screens', function (require) {
"use strict";
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var utils = require('web.utils');
    var Screens = require('point_of_sale.screens');
    var field_utils = require('web.field_utils');

    var QWeb = core.qweb;
    var _t = core._t;
    var BarcodeEvents = require('barcodes.BarcodeEvents').BarcodeEvents;

Screens.PaymentScreenWidget.include({

    init: function(parent, options) {
        var self = this;
        this._super(parent, options);

        this.pos.bind('change:selectedOrder',function(){
                this.renderElement();
                this.watch_order_changes();
            },this);
        this.watch_order_changes();

        this.inputbuffer = "";
        this.firstinput  = true;
        this.decimal_point = _t.database.parameters.decimal_point;
        
        // This is a keydown handler that prevents backspace from
        // doing a back navigation. It also makes sure that keys that
        // do not generate a keypress in Chrom{e,ium} (eg. delete,
        // backspace, ...) get passed to the keypress handler.
        this.keyboard_keydown_handler = function(event){
            if ($('.pay-note').is(':focus')){
                return
            }
            if (event.keyCode === 8 || event.keyCode === 46) { // Backspace and Delete
                event.preventDefault();

                // These do not generate keypress events in
                // Chrom{e,ium}. Even if they did, we just called
                // preventDefault which will cancel any keypress that
                // would normally follow. So we call keyboard_handler
                // explicitly with this keydown event.
                self.keyboard_handler(event);
            }
        };
        
        // This keyboard handler listens for keypress events. It is
        // also called explicitly to handle some keydown events that
        // do not generate keypress events.
        this.keyboard_handler = function(event){
            // On mobile Chrome BarcodeEvents relies on an invisible
            // input being filled by a barcode device. Let events go
            // through when this input is focused.
            if ($('.pay-note').is(':focus')){
                return
            }
            
            if (BarcodeEvents.$barcodeInput && BarcodeEvents.$barcodeInput.is(":focus")) {
                return;
            }

            var key = '';

            if (event.type === "keypress") {
                if (event.keyCode === 13) { // Enter
                    self.validate_order();
                } else if ( event.keyCode === 190 || // Dot
                            event.keyCode === 110 ||  // Decimal point (numpad)
                            event.keyCode === 188 ||  // Comma
                            event.keyCode === 46 ) {  // Numpad dot
                    key = self.decimal_point;
                } else if (event.keyCode >= 48 && event.keyCode <= 57) { // Numbers
                    key = '' + (event.keyCode - 48);
                } else if (event.keyCode === 45) { // Minus
                    key = '-';
                } else if (event.keyCode === 43) { // Plus
                    key = '+';
                }
            } else { // keyup/keydown
                if (event.keyCode === 46) { // Delete
                    key = 'CLEAR';
                } else if (event.keyCode === 8) { // Backspace
                    key = 'BACKSPACE';
                }
            }

            self.payment_input(key);
            event.preventDefault();
        };
    },

    click_please: function(){
        var order = this.pos.get_order();
        
    },
    click_please: function(){
        var order = this.pos.get_order();
        order.set_to_please(!order.is_to_please());
        if (order.is_to_please()) {
            this.$('.js_please').addClass('highlight');
        } else {
            this.$('.js_please').removeClass('highlight');
        }
    },
    renderElement: function() {
        var self = this;
        this._super();
        this.$('.js_please').click(function(){
            self.click_please();
        });
    },

    show_popup_alert: function(title, message) {
        var self = this;
        self.gui.show_popup('confirm', {
            title: title,
            body:  message,
            confirm: function(){
                self.gui.show_screen('clientlist');
            },
        });
    },

    order_is_valid: function(force_validation) {
        var self = this;
        var order = this.pos.get_order();
        if (order.to_please && this.pos.config.please_id){
            var client = order.get_client();
            if (!client){
                this.show_popup_alert('Por favor seleccione el cliente',
                    'Debe seleccionar el cliente antes de poder realizar un pedido.');
                return false;
            }

            if (!client.city_id){
                this.show_popup_alert('Se requier Ciudad',
                    'Debe asignar una ciudad al cliente para el envio de Please API.');
                return false;
            }
            if (!client.street || client.street == ''){
                this.show_popup_alert('Se require Direccion',
                    'Se require Direccion para el envio al cliente mediante Please API');
                return false;
            }
            if (!client.phone){
                this.show_popup_alert('Se require Telefono',
                    'Se require Telefono par el envio al cliente mediante Please API');
                return false;
            }
        }
        return this._super(force_validation);
    },
});

});