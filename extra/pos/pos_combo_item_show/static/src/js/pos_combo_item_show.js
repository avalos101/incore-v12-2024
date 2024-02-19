incore.define('pos_combo_item_show.pos_combo_item_show', function (require) {
"use strict";

    var Screens = require('point_of_sale.screens');
    var Models = require('point_of_sale.models');
    var PopUpWidget=require('point_of_sale.popups');
    var Gui = require('point_of_sale.gui');
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t  = core._t;

    Screens.ProductScreenWidget.include({
        click_product: function(product) {
            var self = this;
            if(product.to_weight && this.pos.config.iface_electronic_scale) {
                this.gui.show_screen('scale', {product: product});
            } else {
                if(product.is_combo){
                    var combo_data = [];
                    for(var i = 0; i < self.pos.get('pack_product').length; i++) {
                        if (self.pos.get('pack_product')[i].product_template_id[0] == product.product_tmpl_id){
                            combo_data.push({
                                'product':self.pos.get('pack_product')[i].product_id[0],
                                'qty':self.pos.get('pack_product')[i].product_quantity,
                                'display_name': self.pos.get('pack_product')[i].product_id[1]
                            })
                        }

                    }
                    self.pos.gui.show_popup('combopack_items',{
                        'combo_data': combo_data,
                        'main_product':product.id,
                        'main_product_name':product.display_name,
                    });
                }
                else{
                    this.pos.get_order().add_product(product);
                } 
            }
        }
    });

    var ComboPackWidget = PopUpWidget.extend({
        template : 'combopack_items',
        show : function(options) {
            var self = this;
            this._super();
            this.combo_data = options.combo_data;
            this.main_product = options.main_product;
            this.main_product_name = options.main_product_name;
            this.renderElement();
        },
        click_confirm: function(){
            var pack_data = [];
            var self = this;
            var product = this.pos.db.get_product_by_id(parseInt($(".combo_product_id").data('product_id')));
            for(var i = 0; i < self.pos.get('pack_product').length; i++) {
                if (self.pos.get('pack_product')[i].product_template_id[0] == product.product_tmpl_id){
                    pack_data.push({
                        'product':self.pos.get('pack_product')[i].product_id[0],
                        'qty':self.pos.get('pack_product')[i].product_quantity,
                        'display_name': self.pos.get('pack_product')[i].product_id[1]
                    })
                }

            }
            var order = this.pos.get('selectedOrder');
            order.add_product(product);
            order.selected_orderline.pack_data = pack_data;
            order.selected_orderline.set_selected();
            this.gui.close_popup();
        },
    });
    Gui.define_popup({name:'combopack_items', widget: ComboPackWidget});

});
