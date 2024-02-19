# -*- coding: utf-8 -*-
import base64
import functools
import os
from datetime import datetime
from random import randrange

import barcode
from barcode.writer import ImageWriter

from incore import fields, models, api


def calculate_checksum(ean):
    sum_ = lambda x, y: int(x) + int(y)
    evensum = functools.reduce(sum_, ean[::2])
    oddsum = functools.reduce(sum_, ean[1::2])
    return (10 - ((evensum + oddsum * 3) % 10)) % 10


def generate_ean13(random=True, prefix=None):
    if prefix:
        if random:
            numbers = [randrange(10) for x in range(8)]
        else:
            numbers = [int(a) for a in datetime.today().strftime('%y%m%d%H')]
        numbers = prefix + numbers
    else:
        if random:
            numbers = [randrange(10) for x in range(12)]
        else:
            numbers = [int(a) for a in datetime.today().strftime('%y%m%d%H%M%S')]
    numbers.append(calculate_checksum(numbers))
    return ''.join(map(str, numbers))


def get_ean13_and_image(category, random=True, prefix=None, ean13=None):
    option = {
        'module_width': category.module_width or 0.2,
        'module_height': category.module_height or 15.0,
        'quiet_zone': category.quiet_zone or 0.0,
        'font_size': category.font_size or 10,
        'text_distance': category.text_distance or 5.0,
        'background': category.background or '#000000',
        'foreground': category.foreground or '#FFFFFF',
        'write_text': category.write_text or False,
    }
    if not ean13:
        ean13 = generate_ean13(random=random, prefix=prefix)
    print("ean13  :  ", ean13)
    ean = barcode.get('ean13', ean13, writer=ImageWriter())
    filename = ean.save('/tmp/' + ean13, options=option)
    print("filename  : ", filename)
    # r = open(filename, 'rb').read()  # .encode('base64')
    r = base64.b64encode(open(filename, 'rb').read())
    os.remove(filename)
    return r, ean13

class ProductTemplate(models.Model):
    _inherit = "product.template"

    ean13_image = fields.Binary("EAN13 image")

    def generate_ean13_barcode(self, barcode=None):
        # Check Context and category
        category = self.env['product.category'].browse(self._context.get('categ_id'))
        if category.use_prefix and category.prefix:
            prefix = [int(a) for a in category.prefix]
            if category.generate_method == 'current_date':
                ean13_image, ean13 = get_ean13_and_image(category, random=False, prefix=prefix, ean13=barcode)
            else:
                ean13_image, ean13 = get_ean13_and_image(category, random=True, prefix=prefix, ean13=barcode)
        else:
            if category.generate_method == 'current_date':
                ean13_image, ean13 = get_ean13_and_image(category, random=False, prefix=None, ean13=barcode)
            else:
                ean13_image, ean13 = get_ean13_and_image(category, random=True, prefix=None, ean13=barcode)

        if not barcode:  # If barcode is passed then return computed ean13 and image
            if not self.search([('barcode', '=', ean13)]):
                return ean13_image, ean13
            else:  # Return False if same barcode is already exist
                return False, False
        else:  # If barcode is passed then return same ean13 and computed image
            return ean13_image, ean13

    @api.model
    def create(self, vals):
        if self._context.get('categ_id'):
            category = self.env['product.category'].browse(self._context.get('categ_id'))
        else:
            category = self.env['product.category']._category_default_get('product.template')
        
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def generate_barcode(self):
        ctx = dict(self._context)
        for product in self:
            ean13 = None
            if product.categ_id:
                ctx.update({'categ_id': product.categ_id.id})
            else:
                category = self.env['product.category']._category_default_get('product.template')
                ctx.update({'category_id': categ_id.id})
            if self._context.get('override_barcode'):
                ean13_image, ean13 = product.with_context(ctx).generate_ean13_barcode()
                while self.search([('barcode', '=', ean13)]):
                    ean13_image, ean13 = product.with_context(ctx).generate_ean13_barcode()
            elif product.barcode:
                if not product.ean13_image:
                    ean13_image, ean13 = product.with_context(ctx).generate_ean13_barcode(product.barcode)
            else:  # Not Barcode:
                ean13_image, ean13 = product.with_context(ctx).generate_ean13_barcode(product.barcode)
                while self.search([('barcode', '=', ean13)]):
                    ean13_image, ean13 = product.with_context(ctx).generate_ean13_barcode(product.barcode)
            if ean13:
                product.write({'barcode': ean13, 'ean13_image': ean13_image})
        return True
