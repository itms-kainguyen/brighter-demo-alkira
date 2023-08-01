{
    'name': 'theme alkira',
    'description': 'this theme is very basic and standard to begin',
    'version': '1.0',
    'author': 'Si Nguyen',
    'data': [],
    'category': 'Theme/Creative',
    'depends': ['base', 'website', 'website_sale'],
    'data': [
        # 'views/header.xml',
        'views/footer.xml',
        'views/home_page.xml',

        
        # menu
        'views/website_data.xml',

        # pages
        'views/temp_page.xml',
        'views/hero_page.xml',
        'views/modal_page.xml',
        'views/badges_page.xml',
        'views/listgroup_page.xml',
        'views/breadcrumbs_page.xml',
        'views/buttons_page.xml',
        'views/album_page.xml',
        'views/pricing_page.xml',
        'views/checkout_page.xml',
        'views/carousel_page.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            # scss
            'theme_alkira/static/scss/style.scss',

            # js
            'theme_alkira/static/js/script.js',

        ],
    },
}
