# -*- coding: utf-8 -*-

# Created on 2017-11-05
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# incore在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# incore10离线中文用户手册下载
# https://www.sunpop.cn/incore10_user_manual_document_offline/
# incore10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（incore开发必备）
# https://www.sunpop.cn/incore10_developer_document_offline/
# description:

def pre_init_hook(cr):
    try:
        cr.execute("UPDATE res_partner "
                   "SET ref = 'P!' || id "
                   "WHERE ref IS NULL OR ref = 'New';")
        cr.execute("UPDATE res_partner "
                   "SET barcode = ref "
                   "WHERE barcode IS NULL OR barcode = 'New';")
    except Exception as e:
        pass

def post_init_hook(cr, registry):
    try:
        pass
    except Exception as e:
        raise Warning(e)
