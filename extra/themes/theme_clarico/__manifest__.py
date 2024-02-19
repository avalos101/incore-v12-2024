{
    # Theme information

    'name': 'Theme Clarico',
    'category': 'Theme/eCommerce',
    'summary': 'Fully Responsive inCore Theme suitable for eCommerce Businesses',
    'version': '12.0.0.15',
    'license': 'OPL-1',	
    'depends': [
        'emipro_theme_base',       
    ],

    'data': [
		'templates/assets.xml',
        'templates/emipro_custom_snippets.xml', 
        'templates/incore_default_snippets.xml',
        'templates/blog.xml',
        'templates/shop.xml',
        'templates/portal.xml',
        'templates/product.xml',
        'templates/cart.xml',
        'templates/quickview.xml',
        'templates/login.xml',
        'templates/theme_customise_option.xml',
	    'templates/404.xml',
        'templates/category.xml',
        'templates/compare.xml',
        'templates/header.xml',
        'templates/footer.xml',
        'templates/customize.xml',
        'templates/menu_config.xml',
        'templates/slider.xml',
        'templates/wishlist.xml',
    	'templates/product_label.xml',
        'templates/contactus.xml',
        'templates/recently_viewed.xml',
        'data/slider_styles_data.xml'
    ],

    #inCore Store Specific
    'live_test_url': 'http://clarico12ee.theme12demo.emiprotechnologies.com',
    'images': [
        'static/description/main_poster.jpg',
        'static/description/main_screenshot.jpg',
    ],
    
    # Author
    'author': 'Emipro Technologies Pvt. ',
    'website': 'https://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. ',

    # Technical
    'installable': True,
    'auto_install': False,
    'price': 299.00,
    'currency': 'EUR',  
}
