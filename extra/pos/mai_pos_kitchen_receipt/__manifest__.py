{
    'name': 'POS Kitchen Receipt || Customised POS Kitchen Receipt',
    'version': '12.0.0.0',
    'sequence': 1,
    'email': 'apps@maisolutionsllc.com',
    'website':'http://maisolutionsllc.com/',
    'category': 'Point of Sale',
    'summary': 'POS Kitchen Receipt OR Customised POS Kitchen Receipt',
    'author': 'MAISOLUTIONSLLC',
    'price': 12,
    'currency': 'EUR',
    'license': 'OPL-1',
    'description': """
    POS Kitchen Receipt OR Customised POS Kitchen Receipt
        """,
    "live_test_url" : "https://youtu.be/E887WiRZhOI",
	"depends" : ['base','point_of_sale'],
	"data": [
		'views/pos_receipt_template.xml',
		'views/pos_config_view.xml'
	],
	'qweb': ['static/src/xml/templates.xml'],
    'images': ['static/description/main_screenshot.png'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
