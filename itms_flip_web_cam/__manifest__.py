# -*- coding: utf-8 -*-
{
    'name': "Flip Web Cam",
    'summary': "Flip Web Cam",
    'description': "Flip Web Cam",
    'category': 'ITMS/ITMS',
    'version': '16.0.2',
    "website": "https://www.itmsgroup.com.au",
    "author": "ITMS Group",
    "license": "AGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail'],
    # always loaded
    'data': [],
    'assets': {
        'web.assets_backend': [
            'itms_flip_web_cam/static/src/scss/call_participant_video.scss',
        ],
        'web.assets_frontend': [
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
