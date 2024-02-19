# -*- coding: utf-8 -*-
{
  "name"                 :  "POS Change Logo",
  "summary"              :  "This module is use to Change company Logo in point of sale.",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "inCore",
  "license"              :  "Other proprietary",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_config_view.xml',
                             'views/template.xml',
                             'security/ir.model.access.csv',
                            ],
  "qweb"                 :  ['static/src/xml/*.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "pre_init_hook"        :  "pre_init_check",
}
