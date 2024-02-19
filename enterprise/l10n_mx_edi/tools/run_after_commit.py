# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import threading
import logging
from decorator import decorator
from incore import api, registry

_logger = logging.getLogger(__name__)

@decorator
def run_after_commit(function, *args, **kwargs):
    """Decorate a method so that it is run after successfully committing the
    current cursor.
    It is useful for cases where you can not rollback the process.
    E.g. send email, sign invoice, web services methods for other systems...
    Such a method::
        @api.run_after_commit
        @api.multi
        def method(self):
            ...
    """
    self, args = args[0], args[1:]

    if (not self.env.context.get('disable_after_commit', True) or
            getattr(threading.currentThread(), 'testing', False)):
        _logger.debug("Method %s.%s called immediately", self, function)
        return function(self, *args, **kwargs)

    dbname = self.env.cr.dbname
    uid = self.env.uid
    context = self.env.context.copy()
    model_name = self._name
    ids = self.ids[:]

    def callback():
        db_registry = registry(dbname)
        with api.Environment.manage(), db_registry.cursor() as new_cr:
            env = api.Environment(new_cr, uid, context)
            function(env[model_name].browse(ids), *args, **kwargs)

    _logger.debug("Method %s.%s will be called after commit", self, function)
    self.env.cr.after('commit', callback)
