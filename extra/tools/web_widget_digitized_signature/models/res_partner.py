from incore import api, fields, models

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'mail.thread']

    digital_signature = fields.Binary(string='Partner Signature',
                                            attachment=True)

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        partner._track_signature(vals, 'digital_signature')
        return partner

    @api.multi
    def write(self, vals):
        self._track_signature(vals, 'digital_signature')
        return super(ResPartner, self).write(vals)
