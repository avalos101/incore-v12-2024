# -*- coding: utf-8 -*-
# Copyright 2017 Hugo Rodrigues
# License BSD-3-Clause
{
    "name": "URL Shorter",
    "summary": "Convert long URLs to shorter ones",
    "version": "12.0.1.0.1",
    "category": "Tools",
    "website": "https://hugorodrigues.net",
    "author": "Hugo Rodrigues",
    "license": "Other OSI approved licence",
    "application": True,
    "installable": True,
    "depends": [
        "base_automation",
        "ipstack_connector"
        ],
    "data": [
        "views/url_shorter_view.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/cron.xml"
        ]
}
