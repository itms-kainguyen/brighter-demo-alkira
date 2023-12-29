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
        'views/about_page.xml',
        'views/explore_page.xml',
        

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
