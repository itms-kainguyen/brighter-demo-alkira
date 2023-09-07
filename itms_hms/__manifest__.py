# -*- coding: utf-8 -*-
{
    'name': "ITMS HMS",
    'summary': "",
    'description': "",
    'category': 'website',
    'version': '16.0.2',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/product_template_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/itms_hms/static/src/scss/style.scss',
        ],
        'web.assets_frontend': [
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
