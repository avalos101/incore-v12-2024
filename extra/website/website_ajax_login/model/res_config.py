# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################
from incore import fields, models
from incore import api
import logging
from incore.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    website_incore_login = fields.Boolean(
        "inCore Login",
    )
    website_facebook_login = fields.Boolean(
        "Facebook Login",
    )
    facebook_client_id = fields.Char(
        "Facebook App ID"
    )
    google_client_id = fields.Char(
        "Google Client ID "
    )
    show_ajax_form_always = fields.Boolean(
        "Pop Up Ajax form if user not logged in, on every web page.")
    wk_block_ui = fields.Boolean(
        "Don't allow user to close the Ajax Pop Up form without login.")
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        google_id = self.env.ref('auth_oauth.provider_google',False)
        facebook_id = self.env.ref('auth_oauth.provider_facebook',False )
        incore_id =  self.env.ref('auth_oauth.provider_incore')
        IrDefault = self.env['ir.default'].sudo()
        show_ajax_form_always = IrDefault.get(
            'res.config.settings',
            'show_ajax_form_always'
        )
        wk_block_ui = IrDefault.get(
            'res.config.settings',
            'wk_block_ui'
        )
        website_incore_login =IrDefault.get(
            'res.config.settings',
            'website_incore_login'
        )
        res.update(
            google_client_id =  google_id.client_id,
            website_incore_login = incore_id.enabled,
            website_facebook_login =  facebook_id.enabled,
            facebook_client_id =  facebook_id.client_id,
            show_ajax_form_always =  show_ajax_form_always,
            wk_block_ui =  wk_block_ui
        )
        return res


    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        icp = self.env['ir.config_parameter']
        IrDefault = self.env['ir.default'].sudo()
        for record in self:
            config = record

            IrDefault.set(
                'res.config.settings',
                'website_incore_login',
                config.website_incore_login
            )
            IrDefault.set(
                'res.config.settings',
                'show_ajax_form_always',
                config.show_ajax_form_always
            )
            IrDefault.set(
                'res.config.settings',
                'wk_block_ui',
                config.wk_block_ui
            )
            facebook_id = self.env.ref('auth_oauth.provider_facebook',False)
            if facebook_id:
                fb_vals = {
                    'enabled': config.website_facebook_login,
                    'client_id': config.facebook_client_id,
                }
                facebook_id.write(fb_vals)
            incore_id = self.env.ref('auth_oauth.provider_incore',False)
            if incore_id:
                incore_vals = {
                    'enabled': config.website_incore_login,
                }
                incore_id.write(incore_vals)

        return True
