# -*- coding: utf-8 -*-

{
  "name"                 :  "inCore Multi Vendor Marketplace",
  "summary"              :  "Enable Online Multi Vendor inCore Marketplace For Sellers To Sale Their Product.",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "inCore. ",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.incore.co/inCore-Multi-Vendor-Marketplace.html",
  "description"          :  """http://incore.co/blog/incore-multi-vendor-marketplace/""",
  "live_test_url"        :  "http://incoredemo.incore.co/?module=incore_marketplace&lifetime=120&lout=1&custom_url=/",
  "depends"              :  [
                             'website_sale',
                             'stock_account',
                             'website_mail',
                             'delivery_hs_code',
                            ],
  "data"                 :  [
                             'security/marketplace_security.xml',
                             'edi/product_status_change_mail_to_admin.xml',
                             'edi/product_status_change_mail_to_seller.xml',
                             'edi/seller_creation_mail_to_admin.xml',
                             'edi/seller_creation_mail_to_seller.xml',
                             'edi/seller_status_change_mail_to_admin.xml',
                             'edi/seller_status_change_mail_to_seller.xml',
                             'edi/order_mail_to_seller.xml',
                             'data/mp_product_demo_data.xml',
                             'data/mp_config_setting_data.xml',
                             'data/seller_payment_method_data.xml',
                             'data/ir_config_parameter_data.xml',
                             'security/ir.model.access.csv',
                             'views/mp_backend_asset.xml',
                             'wizard/server_action_wizard.xml',
                             'wizard/seller_status_reason_wizard_view.xml',
                             'wizard/seller_payment_wizard_view.xml',
                             'wizard/seller_registration_wizard_view.xml',
                             'views/sequence_view.xml',
                             'views/res_config_view.xml',
                             'views/website_config_view.xml',
                             'views/seller_shop_view.xml',
                             'views/res_partner_view.xml',
                             'views/seller_payment_view.xml',
                             'views/mp_stock_view.xml',
                             'views/seller_view.xml',
                             'views/mp_product_view.xml',
                             'views/mp_sol_view.xml',
                             'views/account_invoice_view.xml',
                             'views/seller_review_view.xml',
                             'views/website_mp_product_template.xml',
                             'views/website_mp_template.xml',
                             'views/website_seller_profile_template.xml',
                             'views/website_seller_shop_template.xml',
                             'views/website_account_template.xml',
                             'views/mp_menu_view.xml',
                             'data/marketplace_dashboard_demo.xml',
                             'data/seller_shop_style_data.xml',
                             'data/social_media_data.xml',
                             'views/mp_dashboard_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  299,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}