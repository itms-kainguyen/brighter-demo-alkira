# -*- coding: utf-8 -*-

{
    "name": "ITMS CONSENT FORM",
    "version": "16.0.1.0.0",
    "category": "Tools",
    "summary": "",
    'author': "ITMS Group",
    'website': "https://itmsgroup.com.au",
    "license": "AGPL-3",
    "depends": ["base","document_page","contacts","portal"],
    "data": [
        "security/ir.model.access.csv",
        "views/consent_form_views.xml",
        "views/consent_form_portal_templates.xml",
        "report/ir_actions_report_templates.xml",
        "report/ir_actions_report.xml",
        "data/email.xml",
    ],
    "installable": True,
    "application": True
}
