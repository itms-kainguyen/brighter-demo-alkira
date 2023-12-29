# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>)

{
    'name': 'Send Voice Message',
    'version': '16.0.1.1',
    'summary': '''
        This module helps in adding voice recordings as an attachment in chatter in all documents in odoo
        Chat Voice Recorder
        Voice Chat in Odoo
        odoo chatter message
        voice message in odoo chatter
        add audio message in chatter
        audio message attachment in chattebox
        post message in odoo chatter
        record audio messages for chatter
        send voice message
        send voice recording in chatter
    ''',
    'category': 'Productivity/Discuss',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'description': '''
        Send Voice Message
        Key Features
            -> Send your voice messages in the mail chatter as an attachment.
    ''',
    'images': ['static/src/description/send_voice_message_knk_banner.jpg'],
    'depends': ['mail', 'multi_sms_gateway'],
    'assets': {
        'web.assets_backend': [
            'send_voice_message_knk/static/src/js/composer_view_model.js',
            'send_voice_message_knk/static/src/js/send_sms.js',
            'send_voice_message_knk/static/src/xml/mail.xml',
            'send_voice_message_knk/static/src/xml/send_sms.xml',
            'send_voice_message_knk/static/src/css/main.css',
            'send_voice_message_knk/static/lib/index.js',
        ]
    },
    'installable': True,
    'price': 90,
    'currency': 'EUR',
}
