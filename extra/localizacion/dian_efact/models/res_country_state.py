# -*- coding: utf-8 -*-
from incore import api, fields, models, _
from incore.exceptions import Warning
from incore import http
from pprint import pprint
import importlib
import os, json
from incore.http import request
from lxml import etree
from dianservice.dianservice import Service
import logging

_logger = logging.getLogger(__name__)

class res_country_state(models.Model):
    _inherit = 'res.country.state'    
    
    sector_type = fields.Selection([("state","Estado"),("district","Districto")], default="state")
