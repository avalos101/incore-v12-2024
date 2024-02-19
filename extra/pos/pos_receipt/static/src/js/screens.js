incore.define('pos_receipt.screens', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;

    screens.PaymentScreenWidget.include({
        finalize_validation: function() {
            var self = this;
            var order = this.pos.get_order();
            if (this.pos.config.pos_name_order){

                if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) { 
                    this.pos.proxy.open_cashbox();
                }

                order.initialize_validation_date();
                order.finalized = true;

                if (order.is_to_invoice()) {
                    var invoiced = this.pos.push_and_invoice_order(order);
                    this.invoicing = true;

                    invoiced.fail(this._handleFailedPushForInvoice.bind(this, order, false));

                    invoiced.done(function(){
                        self.invoicing = false;
                        self.gui.show_screen('receipt');
                    });
                } else {
                    var order_c =  this.pos.push_order(order);
                    order_c.fail(this._handleFailedPushForInvoice.bind(this, order, false));
                    order_c.done(function(){
                        self.gui.show_screen('receipt');
                    })
                }
            }
            else{
                this._super();
            }
        },
    })

    screens.ReceiptScreenWidget.include({
        handle_auto_print: function() {
            if (this.should_auto_print()) {
                setTimeout(function () {
                    this.print();
                }, 1000)
                if (this.should_close_immediately()){
                    setTimeout(function () {
                    this.click_next();
                    }, 1500) // TODO: wating 1 second for pos render barcode
                }
            } else {
                this.lock_screen(false);
            }
        },
        
        get_receipt_render_env: function() {
            var res = this._super();
            var website = this.pos.company.website;
            res.url_company = '';
            if (website){
                res.url_company = website.replace('https://','').replace('http://','');
            }
            return res;
        },

        // render_receipt: function () {
        //     this._super();
        //     if (this.pos.config.pos_tiket == '58mm') {
        //         document.getElementById("ticket_custom").classList.replace('pos-sale-ticket','pos-sale-ticket-58');
        //     }
        //     var order = this.pos.get_order();
        //     this.$el.find('#barcode_joy').JsBarcode(order.simplified_invoice, {format: "code128"});
        //     this.$el.find('#barcode_joy').css({
        //         "width": "100%"
        //     });
        // },

        render_receipt: function() {
            var self = this;
            var order = this.pos.get_order();
            if (this.pos.config.pos_name_order) {

                var pushed = new $.Deferred();
                rpc.query({
                    model: 'pos.order',
                    method: 'search_read',
                    domain: [['pos_reference', '=', order['name']]],
                    fields: ['invoice_id','name','sequence_number'],
                }).then(function(orders){
                    if (orders.length > 0 && orders[0]['name']) {
                        var order_name = orders[0]['name'];
                        self.pos.get_order()['order_name'] = order_name;
                    }
                    var ticket = QWeb.render('PosTicket', self.get_receipt_render_env());
                    self.$('.pos-receipt-container').html(ticket);
                    if (self.pos.config.pos_tiket == '58mm') {
                        document.getElementById("ticket_custom").classList.replace('pos-sale-ticket','pos-sale-ticket-58');
                    }
                    var order = self.pos.get_order();
                    self.$el.find('#barcode_joy').JsBarcode(order.order_name, {format: "code128"});
                    self.$el.find('#barcode_joy').css({
                        "width": "100%"
                    });
                    pushed.resolve();
                }).fail(function (error){
                    pushed.reject(error);
                    return pushed;
                });
                return pushed;
            }else {
                this._super();
                if (this.pos.config.pos_tiket == '58mm') {
                    document.getElementById("ticket_custom").classList.replace('pos-sale-ticket','pos-sale-ticket-58');
                }
                var order = this.pos.get_order();
                this.$el.find('#barcode_joy').JsBarcode(order.simplified_invoice, {format: "code128"});
                this.$el.find('#barcode_joy').css({
                    "width": "100%"
                });
            }
        },
    });
});
