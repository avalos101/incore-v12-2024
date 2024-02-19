# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################
{
    'name': 'Website PayuLatam Payment Acquire',
    'author':'BrowseInfo',
    'category': 'eCommerce',
    'website' : "https://www.browseinfo.in",
    'summary': 'PayuLatam Payment Acquirer integration with inCore shop',
    'version': '12.0.0.2',
    'description': """ incore PayuLatam Payment Acquirer incore Pay U Payment Acquirer

    incore Payu-Latam Payment Acquirer
		incore Website PayuLatam Payment Acquirer integration with inCore shop
		incore Website Payment Acquirer PayuLatam Website Latin america payment gateway with incore
		incore Website Latin america payment Acquirer Website Payu Payment Acquirer Website payment payu Acquirer


		incore Website Payu Latam Payment Acquirer integration with inCore shop Website Payment Acquirer Payu Latam
		incore Website Pay u Payment Acquirer Website payment pay u Acquirer

		incore Website Payu-Latam Payment Acquirer integration with inCore shop Website Payment Acquirer Payu-Latam
		incore Website Pay-u Payment Acquirer Website payment pay-u Acquirer

        incore webshop PayuLatam Payment Acquirer integration with webshop incore
        incore webshop Payment Acquirer PayuLatam webshop Latin america payment gateway with incore
        incore webshop Latin america payment Acquirer webshop Payu Payment Acquirer webshop payment payu Acquirer


        incore eCommerce Payu Latam Payment Acquirer integration with inCore shop eCommerce Payment Acquirer Payu Latam
        incore eCommerce Pay u Payment Acquirer Website payment pay u Acquirer

        incore eCommerce Payu-Latam Payment Acquirer integration with inCore eCommerce Payment Acquirer Payu-Latam
        incore eCommerce Pay-u Payment Acquirer eCommerce payment pay-u Acquirer



""",
    'depends': ['payment','website_sale'],
    "price": 45,
    "currency": 'EUR',
    'data': [
        'views/payment_acquirer.xml',
        'views/payment_payulatam_template.xml',
        'data/payu.xml',
    ],
    'installable': True,
    "live_test_url":'https://youtu.be/2I4nu0kib3s',
    "images":["static/description/Banner.png"],
}
