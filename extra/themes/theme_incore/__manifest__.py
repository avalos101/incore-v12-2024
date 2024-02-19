# -*- coding: utf-8 -*-

{
    'name': 'Theme inCore',
    'category': 'Theme/Ecommerce',
    'summary': 'Advanced eCommerce Responsive and Customizable Theme with 170+ Snippets.',
    'version': '3.22',
    'author': 'inCore',
    'sequence': 1000,
	'license' : 'OPL-1',
    'description': """
Theme inCore is  is a inCore theme with advanced ecommerce feature, extremely customizable and fully responsive. It's suitable for any e-commerce sites.
Start your inCore store right away with The inCore theme.
Corporate theme,
Creative theme,
Ecommerce theme,
Education theme,
Entertainment theme,
Personal theme,
Services theme,
Technology theme,
Business theme,
Multipurpose incore theme,
Multi-purpose theme,
        """,
    'depends': ['incore_customize','website_theme_install'],
    'data': [
        'views/customize_template.xml',
        'views/templates.xml',
        'data/theme_incore_data.xml',
    ],
    'live_test_url': 'http://theme-incore.atharvasystem.com/',
	'images': ['static/description/incore_banner.png','static/description/incore_banner_screenshot.png'],
    'application': False,
}
