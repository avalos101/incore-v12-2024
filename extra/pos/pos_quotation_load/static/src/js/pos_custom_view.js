
incore.define('pos_quotation_load.pos', function (require) {
	
    //var bus = require('bus.bus').bus;
    var task;

    var models = require('point_of_sale.models');
	var _super_posmodel = models.PosModel.prototype;
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;

    models.load_fields('pos.order', ['sale_order_id','sale_order_name']);
	
    models.load_models([{
        model: 'sale.order',
        domain: [['state','in',['draft','sent']]],
        loaded: function(self, sale_quotations){
            self.sale_quotations = [];
            if(sale_quotations.length){
                self.sale_quotations = sale_quotations;
            }
        },
    }]);
    
    
    
    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_as_JSON: function() {
        	//$(".set-quotation").html("Load Quotation");
        	var data = _super_order.export_as_JSON.apply(this, arguments);
            data.sale_order_id = this.sale_order_id;
            data.sale_order_name = this.sale_order_name;
            return data;
        },
        init_from_JSON: function(json) {
        	//$(".set-quotation").html("Load Quotation");
            this.sale_order_id = json.sale_order_id;
            this.sale_order_name = json.sale_order_name;
            _super_order.init_from_JSON.call(this, json);
        },
        get_quotation: function(){
            return this.sale_order_name;
        },
        set_quotation: function(sale_order_name) {
            this.sale_order_name = sale_order_name;
            this.trigger('change');
        },        
    });
    
    var LoadQuotationButton = screens.ActionButtonWidget.extend({
        template: 'LoadQuotationButton',
        get_quotation: function() {
            if (this.pos.get_order()) {
            	
                 	return this.pos.get_order().sale_order_name || "Load Quotation";
                 
                 
            } else {
                return "Load Quotation";
            }
            
        },        
        button_click: function() {
        	self = this;
			var order = this.pos.get_order();
            this.gui.show_screen('quotation_products_list');
        },
    });




    screens.define_action_button({
        'name': 'quotation_products_button',
        'widget': LoadQuotationButton,
        'condition': function(){
            return this.pos.config.sh_enable_quotation_load
        },
    });

screens.OrderWidget.include({
    update_summary: function(){
        this._super();
        if (this.getParent().action_buttons &&
            this.getParent().action_buttons.quotation_products_button) {
            this.getParent().action_buttons.quotation_products_button.renderElement();
        }
    },
});

    var QuotationListScreenWidget = screens.ScreenWidget.extend({
        template: 'QuotationListScreenWidget',
        get_all_product_quotations: function(){
            return this.pos.sale_quotations;
        },
        get_quotation_by_name: function(name){
            return _.filter(this.pos.sale_quotations, function(template){
                return template.name === name;
            });
        },
        get_quotation_by_customer: function(name){
            return _.filter(this.pos.sale_quotations, function(template){		
if (template.partner_id[0,1].toLowerCase().indexOf(name.toLowerCase())>-1){
                return true;
}
else{
return false;
}
            });
        },
        get_quotation_by_id: function(id){
        	var params = {
                    model: 'sale.order',
                    method: 'search_read',
                    domain: [['id', '=', id]]
                }
                rpc.query(params, {async: false})
                .then(function(quotation){
                	return template.id === quotation;
                });            
        },
        load_quotation: function(){
            var self = this;
            var order_id = this.$('.quotation-list-contents').find('.quotation-line.highlight').data('id');
            if(order_id){
            	var order = this.pos.get_order();
	        	var quotation = ''
	        	var params = {
	                    model: 'sale.order',
	                    method: 'search_read',
	                    domain: [['id', '=', order_id]]
	                }
	                rpc.query(params, {async: false})
	                .then(function(quotation){
	                	quotation = quotation[0];
	    				order.sale_order_id = order_id;
	    				order.sale_order_name = quotation.name;	
	    				if(quotation.partner_id){
	    					var params = {
	    		                    model: 'res.partner',
	    		                    method: 'search_read',
	    		                    domain: [['id', '=', quotation.partner_id[0]]]
	    		                }
	    		                rpc.query(params, {async: false})
	    		                .then(function(partner){
	    		                	 order.set_client(partner[0]);
	    		                });
	    		           
	    				}
	                    var params = {
	                        model: 'sale.order.line',
	                        method: 'search_read',
	                        domain: [['order_id', '=', order_id]]
	                    }
	                    rpc.query(params, {async: false})
	                    .then(function(quotation_lines){
	                        var order = self.pos.get_order();
	                        if(quotation_lines.length){
	                            _.each(quotation_lines, function(line){
	                                var product_id = line.product_id.length ? line.product_id[0] : false
	                                if(product_id){
	                                    var product = self.pos.db.get_product_by_id(product_id);
	                                    if(product){
	                                        order.add_product(product, {
	                                            quantity: line.product_uom_qty,
	                                            price: line.price_unit,
	                                            discount: line.discount,
	                                        })
	                                    }
	                                }
	                            });
	                        }
	                    });
	                    
	                });
	        	this.gui.back();
        }
        },
        show: function(){
            var self = this;
            this._super();

            this.renderElement();
            this.$('.back').click(function(){
                self.gui.back();
            });
            this.$('.load_quotation').click(function(){
                self.load_quotation();
            });
            var params = {
                    model: 'sale.order',
                    method: 'search_read',   
                    domain: [['state','in',['draft','sent']]],
            }
            rpc.query(params, {async: false}).then(function(quotations){            	
            	self.render_list(quotations);
            });
            this.$('.custom_searchbox input').keypress(function(e){
                if(e.which == 13){
                    $('.custom_searchbox .search-clear').trigger('click');
                }
            })
            this.$('.custom_searchbox .search-clear').click(function(e){
                var $ele = $('.custom_searchbox input')
                if($ele.val()){
                    var search_query = $.trim($ele.val());
                    var selected_quotation = self.get_quotation_by_name(search_query);
                    var selected_quotation_customer = self.get_quotation_by_customer(search_query);
                    if(selected_quotation.length>0){
                        self.render_list(selected_quotation);
                    } 
		else if(selected_quotation_customer.length>0){
			self.render_list(selected_quotation_customer)
		}
		else {
                        alert(_t("No result found!"));
                    }

                } else {
                    var quotations = self.get_all_product_quotations();
                    self.render_list(quotations);
                }
                $ele.val('');
            });
            this.$('.quotation-list-contents').delegate('.quotation-line','click',function(event){
                self.line_select(event,$(this),parseInt($(this).data('id')));
            });
        },
        line_select: function(event,$line,id){		
            this.$('.quotation-list .lowlight').removeClass('lowlight');
            if ( $line.hasClass('highlight') ){
                $line.removeClass('highlight');
                $line.addClass('lowlight');
            }else{
                this.$('.quotation-list .highlight').removeClass('highlight');
                $line.addClass('highlight');
            }
        },
        render_list: function(quotations){
            var contents = this.$el[0].querySelector('.quotation-list-contents');
            contents.innerHTML = "";
            for(var i = 0, len = Math.min(quotations.length,1000); i < len; i++){
                var quotation    = quotations[i];
                var orderline_html = QWeb.render('Quotations',{widget: this, quotation:quotation});
                var orderline = document.createElement('tbody');
                orderline.innerHTML = orderline_html;
                orderline = orderline.childNodes[1];
                contents.appendChild(orderline);
            }
        },
    });
    gui.define_screen({name:'quotation_products_list', widget: QuotationListScreenWidget});
});
