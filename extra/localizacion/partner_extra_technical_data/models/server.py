import logging
from incore import api, fields, models, tools

class Server(models.Model):
    _name = 'partner_extra_technical_data.server'
    _rec_name = 'name'
    _description = 'Info related to servers'

    name = fields.Char(string="Alias del server")
    server_ip = fields.Char('IP Servidor')
    email_account = fields.Char('Email de la cuenta')
    type_login = fields.Selection([('email', 'Ingreso con Email'),('oauth', 'Pantalla OAuth')], string='Tipo de login')
    project_name = fields.Char('Nombre del proyecto') 
