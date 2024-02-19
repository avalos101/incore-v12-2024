from incore import api, fields, models
    
class product_pricelist_item(models.Model):
    _inherit = "product.pricelist.item"
    
    offer_msg = fields.Char(string="Offer Message")