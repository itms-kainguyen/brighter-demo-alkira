# -*- coding: utf-8 -*-
{
    'name': "ITMS HMS",
    'summary': "",
    'description': "",
    'category': 'ITMS/ITMS',
    'version': '16.0.2',
    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail','product','acs_hms','acs_hms_online_appointment'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/calendar_views.xml',
        'views/mail_channel_view.xml',
        'views/ir_attachment_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'itms_hms/static/src/**/*',
        ],
        'web.assets_frontend': [
        ],

    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
