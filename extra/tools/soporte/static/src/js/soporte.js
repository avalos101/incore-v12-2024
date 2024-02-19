incore.define('soporte.soporte', function(require) {
    "use strict";

    var core = require('web.core');
    var mixins = require('web.mixins');
    var rpc = require('web.rpc');
    var Session = require('web.Session');
    var QWeb = core.qweb;
    var _t = core._t;
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');

    var inCoreSoporte = Widget.extend({
        template: 'inCoreSoporte',
        events: {
            "click .oe_activate_soporte": "oe_activate_soporte",
        },
        oe_activate_soporte: function(event) {
            event.preventDefault();
            window.location = $.param.querystring(window.location.href, 'soporte');
        },
    });
    
    rpc.query({
        model: 'res.users',
        method: 'has_group',
        args: ['base.group_system']
    })
    .then(function(is_employee) {
        console.log(is_employee);
        if (is_employee) {
            SystrayMenu.Items.push(inCoreSoporte);
        }
    });
});