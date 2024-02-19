# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import incore
import incore.exceptions

def login(db, login, password):
    res_users = incore.registry(db)['res.users']
    try:
        return res_users._login(db, login, password)
    except incore.exceptions.AccessDenied:
        return False

def check(db, uid, passwd):
    res_users = incore.registry(db)['res.users']
    return res_users.check(db, uid, passwd)

def compute_session_token(session, env):
    self = env['res.users'].browse(session.uid)
    return self._compute_session_token(session.sid)

def check_session(session, env):
    self = env['res.users'].browse(session.uid)
    expected = self._compute_session_token(session.sid)
    if expected and incore.tools.misc.consteq(expected, session.session_token):
        return True
    self._invalidate_session_cache()
    return False
