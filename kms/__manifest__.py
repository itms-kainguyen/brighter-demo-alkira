# -*- coding: utf-8 -*-
{
    'name': 'knowledge management / KMS / Knowledge Base',
    'version': '0.1',
    'category': 'Facility',
    'license': 'OPL-1',
    'price': 25.00,
    'images': ['static/description/kms005.png'],
    'author': 'oranga',
    'currency': 'EUR',
    'summary': 'knowledge management / KMS / Knowledge Base',
    'description': """
    Work Instructions
    Manual Instructions
    Knowledge Management System
    Knowledge base
""",
    'depends': ['base', 'mail'],
    'data': [
        'security/certificate_security.xml',
        'security/ir.model.access.csv',
        'views/letter_print.xml',
        'views/kms_view.xml',
    ],
    'installable': True,
    'application': True,
}