# -*- coding: utf-8 -*-

{
  "name"                 :  "Soporte inCore",
  "summary"              :  "Soporte",
  "category"             :  "web",
  "version"              :  "1.0",
  "author"               :  "inCore",
  "description"          :  """Soporte""",
  "depends"              :  ['web'],
  "data"                 :  ['views/soporte.xml'],
  "qweb"                 :  ['static/src/xml/soporte.xml'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "pre_init_hook"        :  "pre_init_check",
}
