# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from incore import fields, models, api, _
from incore.exceptions import UserError
from incore import SUPERUSER_ID
              

class website(models.Model):
    _inherit = 'website'
    
    def get_website_menu(self):
        menu_ids=self.env['website.menu'].search([('parent_id', '=', False),('website_id','=',self.id)])
        return menu_ids

    def get_website_child_menu(self,parent_id):
        menu_ids=self.env['website.menu'].search([('parent_id', '=', parent_id.id)])     
        return menu_ids
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
