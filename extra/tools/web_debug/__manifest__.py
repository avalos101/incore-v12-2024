# -*- coding: utf-8 -*-

{
  "name"                 :  "Web: inCore Debug Mode",
  "summary"              :  "Allows the admin to enable  debug  in just one click.",
  "category"             :  "web",
  "version"              :  "1.0",
  "author"               :  "inCore",
  "description"          :  """Web: inCore Debug Mode""",
  "depends"              :  ['web'],
  "data"                 :  ['views/web_debug.xml'],
  "qweb"                 :  ['static/src/xml/web_debug.xml'],
  "application"          :  False,
  "installable"          :  True,
  "auto_install"         :  True,
  "pre_init_hook"        :  "pre_init_check",
}
