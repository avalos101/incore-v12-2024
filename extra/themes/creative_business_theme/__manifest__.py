{
    'name': 'Creative Business Theme',
    'summary': 'Creative Business Theme',
    'description': """
    Business Website Theme.

    - Use finely designed building blocks and edit everything inline. 
    - Super Clean Snippets.
    - Fully and Easy Customizable
    - Responsive content on all pages.
    - Edit Anything Inline.
    """,
    'category': 'Theme/Creative',
    'version': '12.0',
    'license': 'LGPL-3',
    'author': 'Key Concepts',
    'website': 'http://keyconcepts.co.in',
    'depends': ['website', 'crm'],
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'views/website_subscribe_view.xml',
        'views/theme_source.xml',
        'views/snippets.xml',
    ],
    "sequence": 1,
    'installable': True,
    'application':True,
    'price': 29,
    'currency': "EUR",
    'images': ['static/description/creative_poster.jpg',
		      'static/description/creative_screenshot.jpg'],
    'live_test_url': 'http://creative.kcits.co.in',
}
