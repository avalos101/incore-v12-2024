# -*- coding: utf-8 -*-

# Created on 2018-11-26
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# incore12在线用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/12.0/en/index.html

# incore12在线开发者手册（长期更新）
# https://www.sunpop.cn/documentation/12.0/index.html

# incore10在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# incore10离线中文用户手册下载
# https://www.sunpop.cn/incore10_user_manual_document_offline/
# incore10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（incore开发必备）
# https://www.sunpop.cn/incore10_developer_document_offline/

{
    'name': 'App Partner Auto Reference,Auto Barcode,Unique Code',
    'summary': """
               Partner Auto code, auto reference. Auto Barcode.
               Customize Sequence for each type partner. like customer [C100001],supplier [S200001]
               add display order of customer and vendor.
               """,
    "version": '12.19.07.14',
    'category': 'Base',
    'author': 'Sunpop.cn',
    'website': 'https://www.sunpop.cn',
    'license': 'AGPL-3',
    'sequence': 2,
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/banner.png'],
    'currency': 'EUR',
    'price': 38,
    'description': """
        App Partner Auto Reference, Auto Barcode, Unique Code,
        add reference code to company.
        客户自动编码，自动条码
    """,
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'depends': [
        'base',
    ],
    'data': [
        # 视图
        'data/partner_sequence.xml',
        'views/res_partner_views.xml',
        'views/res_partner_category_views.xml',
        'views/res_company_views.xml',
    ],
    'demo': [
    ],
}
