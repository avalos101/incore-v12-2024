# -*- coding: utf-8 -*-
import json

from incore import http
from incore.http import request


class Database(http.Controller):
    @http.route('/project_timesheet_synchro/timesheet_app', type='http', auth="user")
    def project_timesheet_ui(self, **kw):
        context = {
            'session_info': json.dumps(request.env['ir.http'].session_info())
        }
        return request.render("project_timesheet_synchro.index", qcontext=context)
