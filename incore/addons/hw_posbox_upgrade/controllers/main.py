# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import logging
import os
import jinja2
import json
import subprocess
import sys
import threading

from incore import http

from incore.addons.hw_proxy.controllers import main as hw_proxy

_logger = logging.getLogger(__name__)

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('incore.addons.hw_posbox_upgrade', "views")

jinja_env = jinja2.Environment(loader=loader, autoescape=True)
jinja_env.filters["json"] = json.dumps

upgrade_page_template = jinja_env.get_template('upgrade_page.html')

class PosboxUpgrader(hw_proxy.Proxy):
    def __init__(self):
        super(PosboxUpgrader,self).__init__()
        self.upgrading = threading.Lock()

    @http.route('/hw_proxy/upgrade', type='http', auth='none', )
    def upgrade(self):
        commit = subprocess.check_output("git --work-tree=/home/pi/incore/ --git-dir=/home/pi/incore/.git log -1", shell=True).decode('utf-8').replace("\n", "<br/>")
        return upgrade_page_template.render({
            'title': "inCore's IoTBox - Software Upgrade",
            'breadcrumb': 'IoT Box Software Upgrade',
            'loading_message': 'Updating IoT box',
            'commit': commit,
        })

    @http.route('/hw_proxy/perform_upgrade', type='http', auth='none')
    def perform_upgrade(self):
        self.upgrading.acquire()
        os.system('/home/pi/incore/addons/point_of_sale/tools/posbox/configuration/posbox_update.sh')
        self.upgrading.release()
        return 'SUCCESS'
