
    incore.define('pos_receipt_note_2.models', function (require) {
        "use strict";
        var models = require('point_of_sale.models');
        var core = require('web.core');
        var qweb = core.qweb;
        var _t = core._t;

    var PosModelSuper = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            models.load_fields('res.company',['street','city','state_id','phone','zip','currency_id', 'email', 'website', 'company_registry', 'vat', 'name', 'phone', 'partner_id' , 'country_id', 'tax_calculation_rounding_method','invoice_id']);
            PosModelSuper.initialize.apply(this, arguments);
        },
    });

    var pos_instance = null;

    function set_client(message)  {
        var data = message.data;
        var partner_info = {
            'id': parseInt(data.partner_id, 10),
            'name': data.name,
            'cedula': data.cedula,
        };
        pos_instance.get('selectedOrder').set_client(partner_info);
        alert(_t('Customer set')); //try to get the focus back
    }

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_as_JSON: function () {
            var json = _super_Order.export_as_JSON.apply(this, arguments);
            if (this.order_name) {
                json.order_name = this.order_name;
            }

            return json;
        },
    });
});
