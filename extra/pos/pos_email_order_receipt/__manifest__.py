# -*- coding: utf-8 -*-
#################################################################################
# Author      : inCore.  (<https://incore.co/>)
# Copyright(c): 2015-Present inCore. 
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.incore.co/license.html/>
#################################################################################
{
  "name"                 :  "POS Email Receipt",
  "summary"              :  "This module allows the seller to send an e-receipt to the customers via email instead of printing one.",
  "category"             :  "Point of Sale",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "inCore. ",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.incore.co/POS-Email-Receipt.html",
  "description"          :  """This module allows the seller to send an e-receipt to the customers via email instead of printing one.""",
  "live_test_url"        :  "http://incoredemo.incore.co/?module=pos_email_order_receipt&version=12.0&custom_url=/pos/auto",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/template.xml',
                             'reports/e_receipt_paperformat.xml',
                             'reports/report_file.xml',
                             'reports/order_report.xml',
                             'edi/pos_email_receipt.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}