# Copyright 2018  <https://incore.co/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import threading


from incore import api

__all__ = ['incore_async_call']


def incore_async_call(target, args, kwargs, callback=None):
    t = threading.Thread(target=incore_wrapper, args=(target, args, kwargs, callback))
    t.start()
    return t


# TODO: is there more elegant way?
def incore_wrapper(target, args, kwargs, callback):
    self = get_self(target)
    with api.Environment.manage(), self.pool.cursor() as cr:
        result = call_with_new_cr(cr, target, args, kwargs)
        if callback:
            call_with_new_cr(cr, callback, (result,))


def get_self(method):
    try:
        # python 3
        return method.__self__
    except:
        # python 2
        return method.im_self


def call_with_new_cr(cr, method, args=None, kwargs=None):
    method_name = method.__name__
    self = get_self(method)
    self = self.with_env(self.env(cr=cr))
    return getattr(self, method_name)(*(args or ()), **(kwargs or {}))
