# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import io

from PIL import Image

from incore.tests.common import HttpCase


class TestImage(HttpCase):
    def test_01_content_image_resize_placeholder(self):
        response = self.url_open('/web/image/0/200x150')
        image = Image.open(io.BytesIO(response.content))
        self.assertEqual(image.size, (200, 150))

        response = self.url_open('/web/image/fake/0/image_small')
        image = Image.open(io.BytesIO(response.content))
        self.assertEqual(image.size, (64, 64))
