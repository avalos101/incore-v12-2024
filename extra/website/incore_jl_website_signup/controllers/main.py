# -*- coding: utf-8 -*-
# Copyright 2020 inCore
# - Manuel Marquez <buzondemam@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from incore import http, _
from incore.addons.auth_signup.controllers.main import AuthSignupHome
from incore.addons.auth_signup.models.res_users import SignupError
from incore.exceptions import UserError
from incore.http import request, route


class AuthSignupHome(AuthSignupHome):

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """

        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang

        partner_title = qcontext.get('titleOptions')
        if partner_title == '1':
            title_mister = request.env.ref(
                'base.res_partner_title_mister')
            values['title'] = title_mister and title_mister.id
            values['gender'] = 'M'
        elif partner_title == '0':
            title_madam = request.env.ref(
                'base.res_partner_title_madam')
            values['title'] = title_madam and title_madam.id
            values['gender'] = 'F'

        name = ''
        if qcontext.get('first_name'):
            values['x_name1'] = qcontext['first_name']
            name += qcontext['first_name']
        if qcontext.get('second_name'):
            values['x_name2'] = qcontext['second_name']
            name += ' %s' % qcontext['second_name']
        if qcontext.get('surname'):
            values['x_lastname1'] = qcontext['surname']
            name += ' %s' % qcontext['surname']
        if qcontext.get('second_surname'):
            values['x_lastname2'] = qcontext['second_surname']
            name += ' %s' % qcontext['second_surname']
        values['name'] = name

        if (qcontext.get('data-protection')
                and qcontext['data-protection'] == '1'):
            values['auth_data_processing'] = True

        if qcontext.get('doctype'):
            values['doctype'] = int(qcontext['doctype'])

        if qcontext.get('xidentification'):
            values['xidentification'] = qcontext['xidentification']

        self._signup_with_values(
            qcontext.get('token'), values)
        request.env.cr.commit()

    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].with_context(
            partner_from_signup=True).sudo().signup(values, token)
        request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
        uid = request.session.authenticate(db, login, password)
        if not uid:
            raise SignupError(_('Authentication Failed.'))

    @route()
    def web_auth_signup(self, *args, **kw):
        res = super().web_auth_signup(*args, **kw)
        document_types = request.env[
            'res.partner'].get_website_sale_document_types()
        res.qcontext.update({
            'document_types': document_types,
        })
        return res

    @route('/web/remember_email', type='http', auth='public', website=True, sitemap=False)
    def remember_email(self, *args, **kw):
        """Manage feature of remembering email to user."""
        qcontext = self.get_auth_signup_qcontext()
        if request.httprequest.method == 'POST':
            if (qcontext.get('xidentification') and qcontext.get('doctype')):
                email = request.env['res.partner'].website_get_email(
                    qcontext['doctype'], qcontext['xidentification'])
                if not email:
                    msg = 'No se encontro ningun email asociado al documento %s' % qcontext['xidentification']
                    response = self.web_auth_reset_password(*args, **kw)
                    response.qcontext.update({'error': msg, 'remember_email': 0})
                    return response
                return http.redirect_with_hash('/web/reset_password?login=%s' % email)

        response = self.web_auth_reset_password(*args, **kw)

        if request.httprequest.method == 'GET':
            document_types = request.env[
                'res.partner'].get_website_sale_document_types()
            msg = _("Introduzca su documento de identidad y le recordaremos su email.")
            response.qcontext.update({
                'remember_email': 1,
                'document_types': document_types,
                'message_remember_email': msg,
            })
        return response

    @route()
    def web_auth_reset_password(self, *args, **kw):
        response = super().web_auth_reset_password(*args, **kw)
        if not kw.get('remember_email'):
            response.qcontext.update({'remember_email': 0})
        return response
