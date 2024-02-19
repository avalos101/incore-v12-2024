# -*- coding: utf-8 -*-
from incore import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _get_category(self):
        return self._context.get('product.template', self.categ_id.id)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    on_product_creation = fields.Boolean('Auto Generate On Creation')
    use_prefix = fields.Boolean('Use 3 Digit Prefix')
    prefix = fields.Char('Barcode Prefix', size=3)
    generate_method = fields.Selection([
        ('random_number', 'Generate EAN13 Using Random Number'),
        ('current_date', 'Generate EAN13 Using Current Date'),
    ], 'Barcode Create Method', required=True, default='random_number')
    module_width = fields.Float('Barcode Width In mm', digits=(16, 2), default=0.2,
                                help='The width of one barcode module in mm as Float. Defaults to 0.2')
    module_height = fields.Float('Barcode Height In mm', digits=(16, 2), default=15.0,
                                 help='The height of the barcode modules in mm as Float. Defaults to 15.0.')
    quiet_zone = fields.Float('Space Before And After Barcode', digits=(16, 2), default=0.0,
                              help='Distance on the left and on the right from the border to the first (last) barcode module in mm as Float')
    background = fields.Char("Barcode Background Color", default='#FFFFFF', help='The background color of the created barcode as string')
    foreground = fields.Char("Barcode Foreground Color", default='#000000', help='The foreground and text color of the created barcode as string')
    write_text = fields.Boolean('Write EAN13 Below Image', default=False)
    font_size = fields.Integer('Font Size Of Text Under Barcode', default=10,
                               help='Font size of the text under the barcode in pt as integer. Defaults 10.')
    text_distance = fields.Float('Distance Between Barcode and Text Under It', digits=(16, 2), default=5.0,
                                 help='Distance between the barcode and the text under it in mm as Float. Defaults to 5.0.')

    @api.multi
    def _check_valid_prefix(self):
        for obj in self:
            if len(obj.prefix) == 3:
                try:
                    prefix = [int(a) for a in obj.prefix]
                except:
                    return False
            else:
                return False
        return True

    _constraints = [(_check_valid_prefix, 'Barcode Prefix Should Be Integer(Number) Only !', ['prefix']), ]



    @api.returns('self', lambda value: value.id)
    def _category_default_get(self, object=False, field=False):
        return self.env['product.template']._get_category()