incore.define('snailmailAccountReportsFollowup.FollowupFormController', function (require) {
"use strict";

var FollowupFormController = require('accountReports.FollowupFormController');

FollowupFormController.include({

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    renderButtons: function ($node) {
        this._super.apply(this, arguments);
        this.$buttons.on('click', '.o_account_reports_followup_send_letter_button',
            this._onSendLetter.bind(this));
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */
    _update: function () {
        this._updateButtons();
        return this._super.apply(this, arguments);
    },
    /**
     * Update the buttons according to followup_level.
     *
     * @private
     */
    _updateButtons: function () {
        if (!this.$buttons) {
            return;
        }
        this._super.apply(this, arguments);
        var followupLevel = this.model.get(this.handle).data.followup_level;
        if (followupLevel.send_letter) {
            this.$buttons.find('button.o_account_reports_followup_send_letter_button')
            .removeClass('btn-secondary').addClass('btn-primary');
        } else {
            this.$buttons.find('button.o_account_reports_followup_send_letter_button')
            .removeClass('btn-primary').addClass('btn-secondary');
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Send the customer statement by Post server-side.
     *
     * @private
     */
    _onSendLetter: function () {
        this.model.doSendLetter(this.handle);
        this._updateButtons();
        var res_id = this.model.get(this.handle, {raw: true}).res_id
        this.do_action('snailmail_account_reports_followup.followup_send', {
            additional_context: {active_ids: [res_id]}
        })
    },
});
});