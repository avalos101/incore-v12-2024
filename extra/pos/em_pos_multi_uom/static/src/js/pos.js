incore.define('em_pos_multi_uom', function (require) {
"use strict";

var models = require('point_of_sale.models');
var chrome = require('point_of_sale.chrome');
var core = require('web.core');
var PosPopWidget = require('point_of_sale.popups');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var gui = require('point_of_sale.gui');
var PosDB = require('point_of_sale.DB');
var screens = require('point_of_sale.screens');
var _t = core._t;

models.load_fields('product.product',['has_multi_uom','multi_uom_ids']);

models.load_models([{
    model: 'product.multi.uom',
    condition: function(self){ return self.config.allow_multi_uom; },
    fields: ['multi_uom_id','price','barcode'],
    loaded: function(self,result){
        if(result.length){
            self.em_uom_list = result;
            self.db.add_barcode_uom(result);
        }
        else{
            self.em_uom_list = [];
        }
    },
    }],{'after': 'pos.category'});

    PosDB.include({
        init: function(options){
            var self = this;
            this.product_barcode_uom = {};
            this._super(options);

        },
        add_products: function(products){
            var self = this;
            this._super(products); 
            
            for(var i = 0, len = products.length; i < len; i++){
                var product = products[i];
                if(product.has_multi_uom && product.multi_uom_ids){
                    var barcod_opt = self.product_barcode_uom;
                    for(var k=0;k<barcod_opt.length;k++){
                        for(var j=0;j<product.multi_uom_ids.length;j++){
                            if(barcod_opt[k].id == product.multi_uom_ids[j]){
                                this.product_by_barcode[barcod_opt[k].barcode] = product;
                            }
                        }
                    }
                }
            }

        },
        add_barcode_uom:function(barcode){
            this.product_barcode_uom = barcode;
        },

    });

    var SuperPosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        scan_product: function(parsed_code){
            var selectedOrder = this.get_order();       
            var product = this.db.get_product_by_barcode(parsed_code.base_code);

            if(!product){
                return false;
            }
            
            if(parsed_code.type === 'price'){
                selectedOrder.add_product(product, {price:parsed_code.value});
            }else if(parsed_code.type === 'weight'){
                selectedOrder.add_product(product, {quantity:parsed_code.value, merge:false});
            }else if(parsed_code.type === 'discount'){
                selectedOrder.add_product(product, {discount:parsed_code.value, merge:false});
            }else{
                var temp =  true;
                var pos_multi_op = this.em_uom_list;
                for(var i=0;i<pos_multi_op.length;i++){
                    if(pos_multi_op[i].barcode == parsed_code.code){
                        temp = false;
                    }
                }
                if(temp){
                    selectedOrder.add_product(product);
                }
                else{
                    selectedOrder.add_product(product, { merge:false});
                }
            }
            var line = selectedOrder.get_last_orderline();
            var pos_multi_op = this.em_uom_list;
            for(var i=0;i<pos_multi_op.length;i++){
                if(pos_multi_op[i].barcode == parsed_code.code){
                    line.set_quantity(1);
                    line.set_unit_price(pos_multi_op[i].price);
                    line.set_product_uom(pos_multi_op[i].multi_uom_id[0]);
                    line.price_manually_set = true;
                }
            }
            return true;
        },
    });

    var MulitUOMWidget = PosPopWidget.extend({
        template: 'MulitUOMWidget',

        renderElement: function(){
            var self = this;
            this._super();
            this.$(".multi_uom_button").click(function(){
                var uom_id = $(this).data('uom_id');
                var price = $(this).data('price');
                var line = self.pos.get_order().get_selected_orderline();
                if(line){
                    line.set_unit_price(price);
                    line.set_product_uom(uom_id);
                    line.price_manually_set = true;
                }
                
                self.gui.show_screen('products');
            });
        },
        show: function(options){
            var self = this;
            this.options = options || {};
            var modifiers_list = [];
            var em_uom_list = this.pos.em_uom_list;
            var multi_uom_ids = options.product.multi_uom_ids;
            for(var i=0;i<em_uom_list.length;i++){
                if(multi_uom_ids.indexOf(em_uom_list[i].id)>=0){
                    modifiers_list.push(em_uom_list[i]);
                }
            }
            options.em_uom_list = modifiers_list;
            this._super(options); 
            this.renderElement();
        },
    });

    gui.define_popup({
        'name': 'multi-uom-widget', 
        'widget': MulitUOMWidget,
    });
    var ChangeUOMButton = screens.ActionButtonWidget.extend({
        template: 'ChangeUOMButton',
        button_click: function(){
            var self = this;
            var line = this.pos.get_order().get_selected_orderline();
            if(line){
                var product = line.get_product();
                if(product.multi_uom_ids.length > 0){
                    self.gui.show_popup('multi-uom-widget',{product:product});
                }
            }
        },
    });

    screens.define_action_button({
        'name': 'changeUOMbutton',
        'widget': ChangeUOMButton,
        'condition': function(){
            return this.pos.config.allow_multi_uom;
        },
    });
    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.call(this,attr,options);
            this.emproduct_uom = '';
        },
        set_product_uom: function(uom_id){
            this.emproduct_uom = this.pos.units_by_id[uom_id];
            this.trigger('change',this);
        },

        get_unit: function(){
            var unit_id = this.product.uom_id;
            if(!unit_id){
                return undefined;
            }
            unit_id = unit_id[0];
            if(!this.pos){
                return undefined;
            }
            return this.emproduct_uom == '' ? this.pos.units_by_id[unit_id] : this.emproduct_uom;
        },

        export_as_JSON: function(){
            var unit_id = this.product.uom_id;
            var json = _super_orderline.export_as_JSON.call(this);
            json.product_uom = this.emproduct_uom == '' ? unit_id.id : this.emproduct_uom.id;
            return json;
        },
        init_from_JSON: function(json){
            _super_orderline.init_from_JSON.apply(this,arguments);
            this.emproduct_uom = json.emproduct_uom;
        },

    });

});

