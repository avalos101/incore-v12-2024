# -*- coding: utf-8 -*-

# Created on 2018-11-26
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# incore在线用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/12.0/en/index.html

# incore在线开发者手册（长期更新）
# https://www.sunpop.cn/documentation/12.0/index.html

# incore在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# incore离线中文用户手册下载
# https://www.sunpop.cn/incore_user_manual_document_offline/
# incore离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（incore开发必备）
# https://www.sunpop.cn/incore_developer_document_offline/
# description:

{
    'name': 'Customize incore OEM (Boost, My incore)',
    'version': '12.20.03.01',
    'author': 'Sunpop.cn',
    'category': 'Productivity',
    'website': 'https://www.sunpop.cn',
    'license': 'LGPL-3',
    'sequence': 2,
    'summary': """    
    Default keep incore Logo. For quick developer. Quick customize, set brand, boost, reset data, debug. Language Switcher. 
    Easy Delete data.reset account chart.
    customize my incore. 
    """,
    'description': """
    App Customize incore (Change Title,Language,Documentation,Quick Debug)
    ============
    White label incore.
    Support incore 13, 12, 11, 10, 9.
    You can config incore, make it look like your own platform.
    1. Deletes incore label in footer
    2. Replaces "incore" in Windows title
    3. Customize Documentation, Support, About links and title in usermenu
    4. Adds "Developer mode" link to the top right-hand User Menu.
    5. Adds Quick Language Switcher to the top right-hand User Menu.
    6. Adds Country flags  to the top right-hand User Menu.
    7. Adds English and Chinese user documentation access to the top right-hand User Menu.
    8. Adds developer documentation access to the top right-hand User Menu.
    9. Customize "My incore.com account" button
    10. Standalone setting panel, easy to setup.
    11. Provide 236 country flags.
    12. Multi-language Support.
    13. Change Powered by incore in login screen.(Please change '../views/app_incore_customize_view.xml' #15)
    14. Quick delete test data in Apps: Sales/POS/Purchase/MRP/Inventory/Accounting/Project/Message/Workflow etc.
    15. Reset All the Sequence to beginning of 1: SO/PO/MO/Invoice...
    16. Fix incore reload module translation bug while enable english language
    17. Stop incore Auto Subscribe(Moved to app_incore_boost)
    18. Show/Hide Author and Website in Apps Dashboard
    19. One Click to clear all data (Sometime pls click twice)
    20. Show quick upgrade in app dashboard, click to show module info not go to incore.com
    21. Can clear and reset account chart. Be cautious
    22. Update online manual and developer document to incore
    23. Add reset or clear website blog data
    24. Customize incore Native Module(eg. Enterprise) Url
    25. Add remove expense data
    26. Add multi uninstall modules
    27. Add incore boost modules link.
    28. Easy Menu manager.
    29. Add Install version in App list. Add Local updatable filter in app list.
    
    This module can help to white label the incore.
    Also helpful for training and support for your incore end-user.
    The user can get the help document just by one click.
    """,
    'images': ['static/description/banner.gif'],
    'depends': [
        'base',
        'web',
        'mail',
        'web_settings_dashboard',
        'iap',
        # 'digest',
        # when enterprise
        # 'web_mobile'
    ],
    'data': [
        'views/app_incore_customize_views.xml',
        'views/app_theme_config_settings_views.xml',
        'views/ir_model_views.xml',
        'views/ir_views.xml',
        # data
        'data/ir_config_parameter.xml',
        'data/ir_module_module.xml',
        # 'data/digest_template_data.xml',
        'data/res_company_data.xml',
        'data/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'js': [],
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': True,
}
