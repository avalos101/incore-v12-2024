incore.define('wer_pos_kitchen_screen.pos', function (require) {
"use strict";

	var gui = require('point_of_sale.gui');
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var PopupWidget = require('point_of_sale.popups');
	var rpc = require('web.rpc');
	var core = require('web.core');

	var _t = core._t;

	screens.ProductScreenWidget.include({
		 events: {
	    	'click .product_list_toggle':'product_list_view',
	    	'click .product_grid_view':'product_grid_view',
	    	'click .add_customer':'quick_customer_create',
	    	'click .add_product':'add_product',
	    	'click .clear_blank_order': 'clear_order',
	    },
	    show: function(){
	    	var self = this;
			self._super();
			var order = self.pos.get_order();
			$('.product_list_toggle').removeClass('highlight');
			$('.product_grid_view').addClass('highlight');
			self.list_view = false;
	    	self.pos.get_order().list_view = false;
	    	var product_list = $(self.pos.chrome.screens.products.product_list_widget.el).find('.product-list');
			product_list.removeClass('list');
		},
		clear_order: function(event){
			var self = this;
			self.gui.show_popup('confirm',{
                'title': _t('Clear Cart?'),
                'body':  _t('You want to clear cart?.'),
                confirm: function(){
                    var order = self.pos.get_order();
					var orderlines = order.get_orderlines();
					var lines_ids = [];
					if(orderlines.length){
						_.each(orderlines,function(item) {
		         			lines_ids.push(item.id);
		         		});
				        _.each(lines_ids,function(id) {
				        	order.remove_orderline(order.get_orderline(id));
				        });
					}
                },
            });
			
		},
	    product_list_view: function(event){
	    	var self = this;
	    	$(event.currentTarget).addClass('highlight');
	    	$('.product_grid_view').removeClass('highlight');
      		var product_list = $(self.pos.chrome.screens.products.product_list_widget.el).find('.product-list');
      		self.list_view = true;
      		self.pos.get_order().list_view = true;
			product_list.addClass('list');
	    },
	    product_grid_view: function(event){
	    	var self = this;
	    	self.list_view = false;
	    	self.pos.get_order().list_view = false;
	    	$(event.currentTarget).addClass('highlight');
	    	$('.product_list_toggle').removeClass('highlight');
	    	var product_list = $(self.pos.chrome.screens.products.product_list_widget.el).find('.product-list');
			product_list.removeClass('list');
	    },
	    quick_customer_create: function(event){
	    	var self = this;
	    	self.pos.gui.show_popup('popup_create_customer');
	    },
	    add_product: function(event){
	    	this.pos.gui.show_popup('popup_create_product')
	    }
    });

	screens.ProductListWidget.include({
		renderElement: function() {
			var self = this;
			this._super();
			var product_list = $('.product-list');
			if(self.pos.chrome.screens && self.pos.chrome.screens.products){
				var list_view = self.pos.chrome.screens.products.list_view;
				if(list_view){
					product_list.addClass('list');
				}else{
					product_list.removeClass('list');
				}
			}
        },
	});

	var popup_create_customer = PopupWidget.extend({
        template: 'popup_create_customer',
        show: function (options) {
            var self = this;
            this.uploaded_picture = null;
            this._super(options);
            var contents = self.$el;
            contents.find('#partner_name').focus()
            contents.scrollTop(0);
            self.$el.find('.image-uploader').on('change', function (event) {
                self.load_image_file(event.target.files[0], function (res) {
                    if (res) {
                        self.$el.find('.client-picture img, .client-picture .fa').remove();
                        self.$el.find('.client-picture').append("<img src='" + res + "'>");
                        self.$el.find('.detail.picture').remove();
                        self.uploaded_picture = res;
                    }
                });
            });
        },
        load_image_file: function (file, callback) {
            var self = this;
            if (!file) {
                return;
            }
            if (file.type && !file.type.match(/image.*/)) {
                return this.pos.gui.show_popup('confirm', {
                    title: 'Error',
                    body: 'Unsupported File Format, Only web-compatible Image formats such as .png or .jpeg are supported',
                });
            }

            var reader = new FileReader();
            reader.onload = function (event) {
                var dataurl = event.target.result;
                var img = new Image();
                img.src = dataurl;
                self.resize_image_to_dataurl(img, 600, 400, callback);
            };
            reader.onerror = function () {
                return self.pos.gui.show_popup('confirm', {
                    title: 'Error',
                    body: 'Could Not Read Image, The provided file could not be read due to an unknown error',
                });
            };
            reader.readAsDataURL(file);
        },
        resize_image_to_dataurl: function (img, maxwidth, maxheight, callback) {
            img.onload = function () {
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                var ratio = 1;

                if (img.width > maxwidth) {
                    ratio = maxwidth / img.width;
                }
                if (img.height * ratio > maxheight) {
                    ratio = maxheight / img.height;
                }
                var width = Math.floor(img.width * ratio);
                var height = Math.floor(img.height * ratio);

                canvas.width = width;
                canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);

                var dataurl = canvas.toDataURL();
                callback(dataurl);
            };
        },
        click_confirm: function () {
        	var self = this;
            var fields = {};
            $('.partner_input').each(function (idx, el) {
                fields[el.name] = el.value || false;
            });
            if (!fields.name) {
            	alert("Please enter customer name!")
            	return
            }
            if (this.uploaded_picture) {
                fields.image = this.uploaded_picture.split(',')[1];
            }
            if (fields['partner_type'] == 'customer') {
                fields['customer'] = true;
            }
            if (fields['property_product_pricelist']) {
                fields['property_product_pricelist'] = parseInt(fields['property_product_pricelist'])
            }
            return rpc.query({
                model: 'res.partner',
                method: 'create_partner',
                args: [fields]
            }).then(function (partner) {
            	self.gui.close_popup();
                console.log('{partner_id} created : ', partner)
            }, function (type, err) {
                if (err.code && err.code == 200 && err.data && err.data.message && err.data.name) {
                    self.pos.gui.show_popup('confirm', {
                        title: err.data.name,
                        body: err.data.message,
                    })
                } else {
                    self.pos.gui.show_popup('confirm', {
                        title: 'Error',
                        body: 'inCore connection fail, could not save'
                    })
                }
            });
            this._super();
        },
    });
    gui.define_popup({name: 'popup_create_customer', widget: popup_create_customer});

    var popup_create_product = PopupWidget.extend({
        template: 'popup_create_product',
        show: function (options) {
            var self = this;
            this.uploaded_picture = null;
            this._super(options);
            var contents = self.$el;
            contents.find('#product_name').focus()
            contents.scrollTop(0);
            contents.find('.image-uploader').on('change', function (event) {
                self.load_image_file(event.target.files[0], function (res) {
                    if (res) {
                        contents.find('.client-picture img, .client-picture .fa').remove();
                        contents.find('.client-picture').append("<img src='" + res + "'>");
                        contents.find('.detail.picture').remove();
                        self.uploaded_picture = res;
                    }
                });
            });
        },
        load_image_file: function (file, callback) {
            var self = this;
            if (!file) {
                return;
            }
            if (file.type && !file.type.match(/image.*/)) {
                return this.pos.gui.show_popup('confirm', {
                    title: 'Error',
                    body: 'Unsupported File Format, Only web-compatible Image formats such as .png or .jpeg are supported',
                });
            }

            var reader = new FileReader();
            reader.onload = function (event) {
                var dataurl = event.target.result;
                var img = new Image();
                img.src = dataurl;
                self.resize_image_to_dataurl(img, 600, 400, callback);
            };
            reader.onerror = function () {
                return self.pos.gui.show_popup('confirm', {
                    title: 'Error',
                    body: 'Could Not Read Image, The provided file could not be read due to an unknown error',
                });
            };
            reader.readAsDataURL(file);
        },
        resize_image_to_dataurl: function (img, maxwidth, maxheight, callback) {
            img.onload = function () {
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                var ratio = 1;

                if (img.width > maxwidth) {
                    ratio = maxwidth / img.width;
                }
                if (img.height * ratio > maxheight) {
                    ratio = maxheight / img.height;
                }
                var width = Math.floor(img.width * ratio);
                var height = Math.floor(img.height * ratio);

                canvas.width = width;
                canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);

                var dataurl = canvas.toDataURL();
                callback(dataurl);
            };
        },
        click_confirm: function () {
            var fields = {};
            var self = this;
            $('.product_input').each(function (idx, el) {
                fields[el.name] = el.value || false;
            });
            if (!fields.name) {
                return self.pos.gui.show_popup('confirm', {
                    title: 'Error',
                    body: 'A Product name is required'
                });
            }
            if (this.uploaded_picture) {
                fields.image = this.uploaded_picture.split(',')[1];
            }
            if (fields['pos_categ_id']) {
                fields['pos_categ_id'] = parseInt(fields['pos_categ_id'])
            }
            fields['available_in_pos'] = true;
            return rpc.query({
                model: 'product.product',
                method: 'create_product',
                args: [fields]
            }).then(function (products) {
            	if(products && products[0]){
            		self.pos.db.add_products(_.map(products, function (product) {
		                product.categ = _.findWhere(self.pos.product_categories, {'id': product.categ_id[0]});
		                return new models.Product({}, product);
		            }));
            		self.pos.chrome.screens.products.product_categories_widget.renderElement()
            	}
            	self.gui.close_popup();
            }, function (type, err) {
                if (err.code && err.code == 200 && err.data && err.data.message && err.data.name) {
                    self.pos.gui.show_popup('confirm', {
                        title: err.data.name,
                        body: err.data.message,
                    })
                } else {
                    self.pos.gui.show_popup('confirm', {
                        title: 'Error',
                        body: 'inCore connection fail, could not save'
                    })
                }
            });
        },
    });
    gui.define_popup({name: 'popup_create_product', widget: popup_create_product});

});
