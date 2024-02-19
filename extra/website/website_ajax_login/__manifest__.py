# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    "name" : "Website Ajax Login/Sign-Up",
    "summary" : "When the user clicks on Login/Sign-Up, the requested form appears in a very nice Ajax popup, integrated with facebook, incore, google+.",
    "category" : "Website",
    "version" : "1.1.2",
    "author" : "inCore",
    "license" : "Other proprietary",
    "depends" :  [
        'website',
        'portal',
        'auth_signup',
        'auth_oauth',
    ],
    "data" : [
        'data/website_ajax_config_demo.xml',
        'view/ajax_login_template.xml',
        'view/res_config.xml',
    ],
    "images" : ['static/description/Banner.png'],
    "application" : True,
    "installable" : True,
    "pre_init_hook" : "pre_init_check",
}
