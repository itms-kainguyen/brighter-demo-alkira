# -*- coding: utf-8 -*-
{
    'name': "ITMS HMS",
    'summary': "",
    'description': "",
    'category': 'website',
    'version': '16.0.2',
    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail','product','acs_hms','acs_hms_online_appointment'],
    # always loaded
    'data': [
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/calendar_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'itms_hms/static/src/scss/style.scss',
            'itms_hms/static/src/js/calendar_model_custom.js',
            'itms_hms/static/src/scss/call_participant_video.scss',
        ],
        'web.assets_frontend': [
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
