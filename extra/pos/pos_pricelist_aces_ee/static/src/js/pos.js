incore.define('pos_pricelist_aces_ee.pos', function (require) {
"use strict";

	var gui = require('point_of_sale.gui');
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var PopupWidget = require('point_of_sale.popups');
	var core = require('web.core');
	var rpc = require('web.rpc');

	var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
    	set_pricelist: function (pricelist) {
    		var self = this;
    		if(pricelist != self.pos.default_pricelist && self.pos.config.use_pricelist){
    			_.each(this.get_orderlines(), function (line) {
    	            line.set_original_price(line.get_display_price());
    	        });
    		}
    		_super_Order.set_pricelist.apply(this, arguments);
    	},
    	add_product: function(product, options){
    		_super_Order.add_product.apply(this, arguments);
    		var selected_line = this.get_selected_orderline();
    		if(selected_line && this.pricelist != this.pos.default_pricelist && this.pos.config.use_pricelist){
    			selected_line.set_original_price(product.get_price(this.pos.default_pricelist, selected_line.get_quantity()))
    		}
    	},
    });

    var _super_orderline = models.Orderline.prototype;
	models.Orderline = models.Orderline.extend({
		set_original_price: function(price){
			this.set('original_price', price)
		},
		get_original_price: function(){
			return this.get('original_price')
		},
		init_from_JSON: function(json) {
			_super_orderline.init_from_JSON.apply(this, arguments)
			this.set_original_price(json.original_price);
		},
		export_for_printing: function() {
            var line = _super_orderline.export_for_printing.apply(this, arguments);
            line.original_price = this.get_original_price() || false;
            return line;
        },
	});

	screens.ScreenWidget.include({
		init: function(parent, options){
			var self = this;
	        this._super(parent, options);
	        this.keydown_pricelist = function(event){
	        	event.stopImmediatePropagation();
	        	self.keyboard_pricelist(event);
	        };
	    },
	    start: function(){
			var self = this;
			this._super();
			if(self.pos.pricelists && self.pos.pricelists.length > 1){
				$(document).keydown(_.bind(this.keydown_pricelist, self));
			}
			
		},
		keyboard_pricelist: function(event){
			var self = this;
			if(self.gui.get_current_screen() === "products"){
				var keytostring = event.key;
				var current_popup = self.gui.current_popup;
				if(keytostring === self.pos.config.open_pricelist_popup){
					self.pos.gui.screen_instances.products.action_buttons.set_pricelist.button_click();
				}
			}
			if(current_popup){
				if(event.keyCode === $.ui.keyCode.ESCAPE){
					current_popup.click_cancel();
				}
				if(event.keyCode === $.ui.keyCode.UP){
					var prev_el = $('.selection-item.selected').prev();
					if(prev_el.length > 0){
						$('.selection-item.selected').removeClass('selected')
						$(prev_el).addClass('selected');
					}
				}
				if(event.keyCode === $.ui.keyCode.DOWN){
					var next_el = $('.selection-item.selected').next();
					if(next_el.length > 0){
						$('.selection-item.selected').removeClass('selected')
						$(next_el).addClass('selected');
					}
				}
				if(event.keyCode === $.ui.keyCode.ENTER){
					var item = current_popup.list[parseInt($('.selection-item.selected').data('item-index'))]
					if(item && item.item){
						current_popup.options.confirm.call(self,item.item);
						current_popup.gui.close_popup();
					}
				}
			}
			
		},
	});
});