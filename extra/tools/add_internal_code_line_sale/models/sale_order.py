# -*- coding: utf-8 -*-
from incore import api, fields, models
import incore.addons.decimal_precision as dp

import re
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    product_add_code = fields.Char(
        string = 'Add Product',
        )
    @api.depends('product_add_code')
    @api.onchange('product_add_code')
    def _add_line_code_default(self):
        ### Esta funcion extiende las ventas y agrega un campo de coigo interno del producto para agregar lineas a partir de aqui
        if self.product_add_code == False:pass
        elif self.partner_id :
            print(type(self.product_add_code), self.product_add_code)
            code_por_qty = self.product_add_code
            
            find_code_por_qty = code_por_qty.find("**")
            #print("Find: ", find_code_por_qty)
            if find_code_por_qty != -1:
                code_default = code_por_qty[0:find_code_por_qty]
                cantidad = float(code_por_qty[find_code_por_qty+2:])

            else:
                code_default = self.product_add_code
                cantidad = 1
            #print("Codigo:", code_default, "Cantidad: ",  cantidad)
            class_product_template = self.env['product.product']
            #code_product = class_product_template.search([('default_code', '=', code_default)])
            
            code_product = class_product_template.search([('default_code', '=', code_default), ])
            if  len(code_product) ==0:
                #print("NOOOO")
                code_product = class_product_template.search([('default_code', '=', code_default.lower()), ])
            if  len(code_product) ==0:
                #print("NOOOO")
                code_product = class_product_template.search([('default_code', '=', code_default.upper()), ])
            if  len(code_product) ==0:
                
                code_product_ilike = class_product_template.search([('default_code', 'ilike', code_default), ])
                #print(code_product_ilike)
                for code in code_product_ilike:
                    print(code.default_code ,code_default)
                    if re.search( code.default_code ,code_default, re.IGNORECASE):
                        code_product = class_product_template.browse(code.id)
            
            #order_sale = class_sale_order.search([('id', '=', self.id)])
            if len(code_product)!= 0  and self.partner_id:
                #print("Tipo de Orden:, ")
                list_data = []
                if code_product[0].description_sale:
                    name = "["+code_product[0].default_code + "]" + code_product[0].name + code_product[0].description_sale
                else:
                    name = "["+code_product[0].default_code + "]" + code_product[0].name
                    
                new_lines = {
                                    'name' : name ,
                                    'product_uom_qty' : cantidad,
                                    'product_uom' : code_product[0].uom_id.id,
                                    'product_id' :code_product[0].id,
                                    'tax_id' :code_product[0].taxes_id,
                                    }
                if self.pricelist_id and code_product[0].pricelist_item_ids:
                    
                    list_price_product = code_product[0].pricelist_item_ids
                    count = 0
                    for tarifa in list_price_product:
                        print( "DATA: ",  tarifa.pricelist_id.name  )
                        print( "DATA: ",  self.pricelist_id.name )

                        if  self.pricelist_id.name  == tarifa.pricelist_id.name:
                            new_lines['price_unit'] = tarifa.fixed_price
                            new_lines['list_price'] = self.pricelist_id.id
                            count += 1
                    if count ==0:
                        new_lines['price_unit'] = code_product[0].list_price
                        new_lines['list_price'] = self.pricelist_id.id
                
                    
                else:
                    new_lines['price_unit'] = code_product[0].list_price
                    new_lines['list_price'] = self.pricelist_id.id
                    
                
                if self.order_line:
                    #print("Si existe")
                    for line in self.order_line:
                        name_product = line.name
                        product_uom_qty = line.product_uom_qty
                        product_uom = line.product_uom.id
                        product_id = line.product_id.id
                        price_unit = line.price_unit
                        list_price = line.list_price
                        tax_id   = line.tax_id
                        dict_dat = {  
                                    'name' : name_product,
                                    'product_uom_qty' : product_uom_qty,
                                    'product_uom' : product_uom,
                                    'product_id' :product_id,
                                    'price_unit' :price_unit,
                                    'list_price' : list_price,
                                    'tax_id' : tax_id,
                                    }
                        #print(dict_dat)
                        list_data.append([0, 0, dict_dat])
                    list_data.append([0, 0, new_lines])
                    #print(list_data)
                else:
                    list_data.append([0, 0, new_lines])
                self.update({'order_line': list_data })
                
                #self._onchange_price_list()
                
    
    