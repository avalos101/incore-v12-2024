# -*- coding: utf-8 -*-

import hashlib
import logging
from incore import api, fields, models, _
from incore.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _addi_form_get_tx_from_data(self, data):
        orderId = data.get('orderId')
        if not orderId:
            error_msg = 'addi: received data with missing orderId (%s)' % orderId
            _logger.info(error_msg)


        tx = self.search([('reference', '=', orderId)])
        if not tx or len(tx) > 1:
            error_msg = 'addi: received data for reference %s' % (
                orderId)
            if not tx:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return tx

    @api.multi
    def _addi_form_get_invalid_parameters(self, data):
        """Find invalid parameters comming from data of addi."""
        invalid_parameters = []
        if self.acquirer_reference and data.get('orderId') != self.acquirer_reference:
            invalid_parameters.append(('orderId', data.get('orderId'), self.acquirer_reference))
        return invalid_parameters

    def _addi_form_validate(self, data):
        status = data.get('status', 'PENDING')
        _logger.info('\n\n %r \n\n', data)
        if status == 'APPROVED':
            self.write({'acquirer_reference': data.get('orderId')})
            self._set_transaction_done()
            return True
        elif status == 'PENDING':
            self.write({'acquirer_reference': data.get('orderId')})
            self._set_transaction_pending()
            return True
        else:
            dic = {
                "REJECTED" : "La aplicación de crédito en línea es rechazada. El cliente no ha sido aprobado para obtener un crédito con ADDI.",
                "ABANDONED" : "La aplicación de crédito en línea superó el límite máximo de tiempo para su ejecución en la plataforma ADDI.",
                "DECLINED" : "La aplicación de crédito en línea es declinada por el cliente.",
                "METHOD_UNSUPPORTED" : "En el momento no es posible continuar con la aplicación. El cliente debe ser redirijido a seleccionar un método de pago diferente a ADDI en el eCommerce.",
                "INTERNAL_ERROR" : "Ha sucedido un error en la plataforma de ADDI. El cliente debe ser redirijido a seleccionar un método de pago diferente a ADDI en el eCommerce.",
            }
            _logger.info(dic.get(status,'ADDI: feedback error'))
            self.write({'state_message': dic.get(status,'ADDI: feedback error')})
            self._set_transaction_cancel()
        return True