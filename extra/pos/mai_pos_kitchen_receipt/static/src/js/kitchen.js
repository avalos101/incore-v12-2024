incore.define('mai_pos_session_report.mai_pos_kitchen_receipt', function(require){
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var gui = require('point_of_sale.gui');
    var QWeb = core.qweb;
    var CustomKitchenScreen = screens.ReceiptScreenWidget.extend({
        template: 'CustomKitchenScreen',
        click_next: function(){
            this.gui.show_screen('products');
        },
        click_back: function(){
            this.gui.show_screen('products');
        },
        render_receipt: function(){
            order = this.pos.get_order();
            var report = QWeb.render('OrderKitchenReceipt', {
                widget: this,
                pos: this.pos,
                order: order,
                receipt: order.export_for_printing(),
                orderlines: order.get_orderlines(),
                paymentlines: order.get_paymentlines(),
            });
            self.$('.pos-receipt-container').html(report);
        },
        print_web: function(){
            window.print();
        },
    });

    gui.define_screen({name:'session-receipt', widget: CustomKitchenScreen});
    var KitchenReceiptButton = screens.ActionButtonWidget.extend({
        template: 'KitchenReceiptButton',
        button_click: function(){
            this.gui.show_screen('session-receipt');
        },
    });

    screens.define_action_button({
        'name': 'Kitchen Report',
        'widget': KitchenReceiptButton,
        'condition': function(){
            return this.pos.config.print_kitchen_receipt;
        },
    });

});
