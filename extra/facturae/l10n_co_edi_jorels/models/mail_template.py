# -*- coding: utf-8 -*-
#
# Jorels S.A.S. - Copyright (2019-2022)
#
# This file is part of l10n_co_edi_jorels.
#
# l10n_co_edi_jorels is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# l10n_co_edi_jorels is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with l10n_co_edi_jorels.  If not, see <https://www.gnu.org/licenses/>.
#
# email: info@jorels.com
#

import base64
import tempfile
import zipfile
from pathlib import Path

from incore import models, api
from incore.tools import pycompat


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    @api.multi
    def generate_email(self, res_ids, fields=None):
        res = super(MailTemplate, self).generate_email(res_ids, fields)

        self.ensure_one()

        multi_mode = True
        if isinstance(res_ids, pycompat.integer_types):
            res_ids = [res_ids]
            multi_mode = False

        if self._context.get('active_model') == 'account.invoice':
            for res_id, template in self.get_email_template(res_ids).items():
                inv_default_template = self.env.ref('account.email_template_edi_invoice')
                ei_template = self.env.ref('l10n_co_edi_jorels.email_template_edi')
                if template.id in (ei_template.id, inv_default_template.id):
                    invoice = self.env['account.invoice'].browse(res_id)

                    if not invoice.company_id.ei_enable:
                        continue

                    res_t = multi_mode and res[res_id] or res

                    if 'attachments' not in res_t:
                        res_t['attachments'] = []
                    attachments = res_t['attachments'] if invoice.company_id.ei_include_pdf_attachment else []

                    if invoice.is_to_send_edi_email():
                        if invoice.ei_zip_name:
                            attached_document_name = 'ad' + invoice.ei_zip_name[1:-4]
                        else:
                            attached_document_name = invoice.ei_uuid

                        pdf_name = attached_document_name + '.pdf'
                        pdf_path = Path(tempfile.gettempdir()) / pdf_name

                        xml_name = attached_document_name + '.xml'
                        xml_path = Path(tempfile.gettempdir()) / xml_name

                        zip_name = attached_document_name + '.zip'
                        zip_path = Path(tempfile.gettempdir()) / zip_name

                        zip_archive = zipfile.ZipFile(zip_path, 'w')

                        pdf_handle = open(pdf_path, 'wb')
                        pdf_handle.write(base64.decodebytes(res_t['attachments'][0][1]))
                        pdf_handle.close()
                        zip_archive.write(pdf_path, arcname=pdf_name)

                        xml_handle = open(xml_path, 'wb')
                        xml_handle.write(base64.decodebytes(invoice.ei_attached_document_base64_bytes))
                        xml_handle.close()
                        zip_archive.write(xml_path, arcname=xml_name)

                        zip_archive.close()

                        with open(zip_path, 'rb') as f:
                            attached_zip = f.read()
                            ei_attached_zip_base64_bytes = base64.encodebytes(attached_zip)
                            attachments += [(zip_name, ei_attached_zip_base64_bytes)]
                            invoice.write({
                                'ei_attached_zip_base64_bytes': ei_attached_zip_base64_bytes
                            })

                        res_t["attachments"] = attachments

        elif self._context.get('active_model') == 'l10n_co_edi_jorels.radian':
            for res_id, template in self.get_email_template(res_ids).items():
                radian = self.env['l10n_co_edi_jorels.radian'].browse(res_id)

                if not radian.company_id.ei_enable:
                    continue

                res_t = multi_mode and res[res_id] or res

                if 'attachments' not in res_t:
                    res_t['attachments'] = []
                attachments = res_t['attachments'] if radian.company_id.ei_include_pdf_attachment else []
                # attachments = []

                if radian.edi_is_valid \
                        and radian.state == 'posted'\
                        and radian.edi_uuid\
                        and radian.edi_attached_document_base64:

                    if radian.edi_zip_name:
                        attached_document_name = 'ad' + radian.edi_zip_name[1:-4]
                    else:
                        attached_document_name = radian.edi_uuid

                    # pdf_name = attached_document_name + '.pdf'
                    # pdf_path = Path(tempfile.gettempdir()) / pdf_name

                    xml_name = attached_document_name + '.xml'
                    xml_path = Path(tempfile.gettempdir()) / xml_name

                    zip_name = attached_document_name + '.zip'
                    zip_path = Path(tempfile.gettempdir()) / zip_name

                    zip_archive = zipfile.ZipFile(zip_path, 'w')

                    # pdf_handle = open(pdf_path, 'wb')
                    # pdf_handle.write(base64.decodebytes(res_t['attachments'][0][1]))
                    # pdf_handle.close()
                    # zip_archive.write(pdf_path, arcname=pdf_name)

                    xml_handle = open(xml_path, 'wb')
                    xml_handle.write(base64.decodebytes(radian.edi_attached_document_base64))
                    xml_handle.close()
                    zip_archive.write(xml_path, arcname=xml_name)

                    zip_archive.close()

                    with open(zip_path, 'rb') as f:
                        attached_zip = f.read()
                        edi_attached_zip_base64 = base64.encodebytes(attached_zip)
                        attachments += [(zip_name, edi_attached_zip_base64)]
                        radian.write({
                            'edi_attached_zip_base64': edi_attached_zip_base64
                        })

                    res_t["attachments"] = attachments

        return res
