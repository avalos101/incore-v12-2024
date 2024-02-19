# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "POS Quotation Load",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Point of Sale",
    "summary": "POS Quotation Load incore, POS Order So Load incore, Point Of Sale Quotation Load,POS Sales Order Load,POS quotation Analysis Module, Point Of Sale SO Load App, POS Load Sale Order incore",    
    "description": """Do you want to load a quotation to POS? Do you do that manually? so it's quite a time-consuming task, here we build a module to easily load a quotation in POS. Easy to sync quotation with the POS system. You will also easily search quotations in pos. We have also given a field in quotation to identify quotation sync with pos. You can also get a pos order reference number in the quotation. the quotation will be canceled automatically after the POS order is done.            				
POS Quotation Load incore, POS Order So Load incore.
Quotation Load  In Point Of Sale, Sales Order Load In POS Detail Report incore, Feature Of Load SO In POS incore.
POS quotation Analysis Module, Point Of Sale SO Load App, POS Load Sale Order incore.""",
    "version":"12.0.2",
    "depends" : ["sale_management", "point_of_sale"],
    "application" : True,
    "data" : [
                'views/pos_custom_view.xml',
                'views/pos_order_custom_view.xml',
                'views/sale_order_custom.xml',
            ],
    "qweb": [
                "static/src/xml/*.xml",
    	    ],
    "images": ["static/description/background.jpg",],
    "live_test_url": "https://www.youtube.com/watch?v=5U3vS-U5zQo&feature=youtu.be",
    "auto_install":False,
    "installable" : True,
    "price" : 25,
    "currency" : "EUR"  
}
