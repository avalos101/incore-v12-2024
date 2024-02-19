incore.define('project_timesheet_synchro.Session', function (require) {
"use strict";

var Session = require('web.Session');


// Includes the Session only for non-desktop mode.
// Force 'session_reload' to request the server as in 9.0.
// In 'desktop' mode we can avoid this rpc by retrieving the 'session_info'
// from the session (server side) but it's not posssible to do this as
// Awesome Timesheet is a standalone app and templates where we usally store
// 'session_info' aren't generated by the server.
Session.include({
    session_reload: function () {
        var self = this;
        return this.rpc("/web/session/get_session_info", {}).then(function (result) {
            delete result.session_id;
            _.extend(self, result);
        });
    },
});

});
