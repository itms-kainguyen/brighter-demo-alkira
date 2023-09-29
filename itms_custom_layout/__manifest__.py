# -*- coding: utf-8 -*-
{
    'name': "ITMS custom layout",
    'summary': "ITMS custom layout",
    'description': "ITMS custom layout",
    'category': 'ITMS/ITMS',
    'version': '16.0.2',
    "website": "https://www.itmsgroup.com.au",
    "author": "ITMS Group",
    "license": "AGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail', 'sale'],
    # always loaded
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'itms_custom_layout/static/src/scss/itms_custom_layout.scss',
            'itms_custom_layout/static/src/js/itms_custom_layout.js',
            'itms_custom_layout/static/src/views/form/button_box/button_box.xml',
        ],
        'web.assets_frontend': [
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
