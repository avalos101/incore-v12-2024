incore.define('iap.redirect_incore_credit_widget', function(require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');


var IapinCoreCreditRedirect = AbstractAction.extend({
    template: 'iap.redirect_to_incore_credit',
    events : {
        "click .redirect_confirm" : "incore_redirect",
    },
    init: function (parent, action) {
        this._super(parent, action);
        this.url = action.params.url;
    },

    incore_redirect: function () {
        window.open(this.url, '_blank');
        this.do_action({type: 'ir.actions.act_window_close'});
        // framework.redirect(this.url);
    },

});
core.action_registry.add('iap_incore_credit_redirect', IapinCoreCreditRedirect);
});
