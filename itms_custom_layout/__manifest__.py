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
            'itms_custom_layout/static/src/views/mail/static/src/components/channel_member_list/channel_member_list.xml',
            'itms_custom_layout/static/src/views/mail/static/src/components/thread_view_topbar/thread_view_topbar.xml',
        ],
        'web.assets_frontend': [
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
