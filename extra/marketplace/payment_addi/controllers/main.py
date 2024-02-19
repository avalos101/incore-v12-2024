# -*- coding: utf-8 -*-

import json
import werkzeug
from incore import http
from incore.http import request, JsonRequest, Response
from incore.tools import date_utils
from incore.addons.payment.models.payment_acquirer import ValidationError
import logging
_logger = logging.getLogger(__name__)


class AddiController(http.Controller):
    _accept_url = '/payment/addi/accept'
    _decline_url = '/payment/addi/decline'
    _exception_url = '/payment/addi/exception'
    _cancel_url = '/payment/addi/cancel'

    @http.route(['/payment/addi/redirect'], type='http', auth='public', methods=["POST"], csrf=False, website=True)
    def redirect_addi(self, **post):
        acquirer_id = int(post.get('acquirer_id'))
        acquirer = request.env['payment.acquirer'].browse(acquirer_id)
        result = acquirer.addi_initTransaction(post)
        if result:
            return werkzeug.utils.redirect(result)

    def alternative_json_response(self, result=None, error=None):
        if error is not None:
            response = error
        if result is not None:
            response = result
        mime = 'application/json'
        body = json.dumps(response, default=date_utils.json_default)
        return Response(body, status=error and error.pop('http_status', 200) or 200, headers=[('Content-Type', mime), ('Content-Length', len(body))])


    def _post_process_addi_tx(self, data):
        """Post process transaction to confirm the sale order and
        to generate the invoices if needed."""
        tx_reference = data.get('orderId')
        payment_transaction = request.env['payment.transaction'].sudo()

        tx = payment_transaction.search([('reference', '=', tx_reference)])

        if not tx:
            _logger.exception('Transaction post processing failed. '
                              'Not found any transaction with reference %s',
                              tx_reference)

        if tx.state == 'done':
            return tx.sudo()._post_process_after_done()
        elif tx.state != 'pending':
            return tx.sudo()._log_payment_transaction_received()

    @http.route(['/payment/addi/notify'], type='json', auth='public', methods=['POST'], csrf=False, website=True)
    def addi_validate_data(self, **post):
        data = json.loads(request.httprequest.data)
        _logger.info('\n\n\n valores:%r  \n\n', data)
        request._json_response = self.alternative_json_response.__get__(request, JsonRequest)
        data_json = json.dumps(data)
        tx_data = data
        request.env['payment.transaction'].sudo().form_feedback(tx_data, 'addi')
        self._post_process_addi_tx(data)
        return data

    @http.route(['/payment/addi/return'], type='http', auth='public', csrf=False, website=True, methods=['POST','GET'])
    def addi_form_feedback(self, **post):
        # data = json.loads(request.httprequest.data)
        # _logger.info('\nAqui se debe generar la transacción\n %s\n\n', data)
        _logger.info('\nAqui se debe generar la transacción\n %s\n\n', post)
        return werkzeug.utils.redirect('/payment/process')
        # return werkzeug.utils.redirect('/shop/confirmation')
