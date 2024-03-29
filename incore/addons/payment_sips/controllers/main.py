# -*- coding: utf-8 -*-

# Copyright 2015 Eezee-It

import json
import logging
import werkzeug

from incore import http
from incore.http import request

_logger = logging.getLogger(__name__)


class SipsController(http.Controller):
    _notify_url = '/payment/sips/ipn/'
    _return_url = '/payment/sips/dpn/'

    def sips_validate_data(self, **post):
        sips = request.env['payment.acquirer'].search([('provider', '=', 'sips')], limit=1)
        security = sips.sudo()._sips_generate_shasign(post)
        if security == post['Seal']:
            _logger.debug('Sips: validated data')
            return request.env['payment.transaction'].sudo().form_feedback(post, 'sips')
        _logger.warning('Sips: data are corrupted')
        return False

    @http.route([
        '/payment/sips/ipn/'],
        type='http', auth='none', methods=['POST'], csrf=False)
    def sips_ipn(self, **post):
        """ Sips IPN. """
        self.sips_validate_data(**post)
        return ''

    @http.route([
        '/payment/sips/dpn'], type='http', auth="none", methods=['POST'], csrf=False)
    def sips_dpn(self, **post):
        """ Sips DPN """
        try:
            self.sips_validate_data(**post)
        except:
            pass
        return werkzeug.utils.redirect('/payment/process')
