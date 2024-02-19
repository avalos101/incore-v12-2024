incore.define('please_api.models', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    models.load_fields('res.city', [] );
    models.load_fields('res.partner', ['city_id','state_id'] );
    models.load_fields('account.journal', ['upon_delivery'] );
    var modelss = models.PosModel.prototype.models;

    modelss.push({
        model:  'res.city',
            fields: [],
            loaded: function(self, province){
            self.province = province;
        },
    });

    var _super_paymentline = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
        export_as_JSON: function () {
            var json = _super_paymentline.export_as_JSON.apply(this, arguments);
            json.upon_delivery = this.cashregister.journal.upon_delivery;
            return json;
        },
        export_for_printing: function(){
            var json = _super_paymentline.export_for_printing.apply(this,arguments);
            json.upon_delivery = this.cashregister.journal.upon_delivery;
            return json;
        },
    });


    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attributes,options){
            this.to_please = false;
            return _super_Order.initialize.apply(this, arguments);
        },
        set_to_please: function(to_please) {
            this.assert_editable();
            this.to_please = to_please;
        },
        is_to_please: function(){
            return this.to_please;
        },
        init_from_JSON: function(json) {
            this.to_please = false; // FIXED
            _super_Order.init_from_JSON.call(this, json);
        },
        export_as_JSON: function () {
            var json = _super_Order.export_as_JSON.apply(this, arguments);
            json.to_please = this.to_please ? this.to_please : false;
            var note = $('.pay-note').val();
            var city_name = this.get_client() ? this.get_client().city_id[1] : '';
            json.note = note ? note : '';
            if (json.to_please) {
                json.note += ', Ubicacion ' + city_name;
            }
            return json;
        },
        export_for_printing: function(){
            var json = _super_Order.export_for_printing.apply(this,arguments);
            var note = $('.pay-note').val();
            var city_name = '';
            if (this.to_please) {
                city_name = ', Ubicacion ' + this.get('client').city_id[1];
            }
            json.note = {
                note: note ? note : '' + city_name,
            };
            return json;
        },
    });
});
