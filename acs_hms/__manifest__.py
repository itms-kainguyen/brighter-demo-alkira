# -*- coding: utf-8 -*-
{
    'name': 'Brighter Clinic Management System',
    'summary': 'Brighter Clinic Management System',
    'description': """

    """,
    'version': '1.3.28',
    'category': 'ITMS',
    'author': 'ITMSGROUP',
    'license': 'OPL-1',
    'depends': ['base', 'web', 'itms_consent_form', 'acs_hms_base', 'web_timer_widget', 'website', 'digest', 'survey', 'hr_timesheet'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'report/patient_cardreport.xml',
        'report/report_medical_advice.xml',
        'report/report_prescription.xml',
        'report/appointment_report.xml',
        'report/evaluation_report.xml',
        'report/treatment_report.xml',
        'report/procedure_report.xml',
        'report/medicines_label_report.xml',

        'data/sequence.xml',
        'data/mail_template.xml',
        'data/hms_data.xml',
        'data/digest_data.xml',
        'wizard/schedule_consent_view.xml',
        'wizard/cancel_reason_view.xml',
        'wizard/pain_level_view.xml',
        'wizard/reschedule_appointments_view.xml',
        'wizard/multiple_consent_views.xml',
        'wizard/multiple_aftercare_views.xml',
        'wizard/picture_before.xml',
        'wizard/pay_prescriber_view.xml',
        'views/checklist.xml',
        'views/hms_base_views.xml',
        'views/patient_view.xml',
        'views/physician_view.xml',
        'views/evaluation_view.xml',
        'views/treatment_view.xml',
        'views/appointment_view.xml',
        'views/diseases_view.xml',
        'views/medicament_view.xml',
        'views/prescription_view.xml',
        'views/medication_view.xml',
        'views/procedure_view.xml',
        'views/resource_cal.xml',
        'views/medical_alert.xml',
        'views/account_view.xml',
        'views/product_kit_view.xml',
        'views/template.xml',
        'views/res_config_settings_views.xml',
        'views/digest_view.xml',
        'views/res_users.xml',
        'views/menu_item.xml',
        'views/hr_employee.xml',
        'views/survey_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'acs_hms/static/src/js/hms_graph_field.js',       
            'acs_hms/static/src/js/hms_graph_field.xml',
            'acs_hms/static/src/js/hms_graph_field.scss',
            'acs_hms/static/src/scss/custom.scss',
            'acs_hms/static/src/xml/**/*',

            'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.2.1/flowbite.min.js',   
            # 'https://cdnjs.cloudflare.com/ajax/libs/jquery-datetimepicker/2.5.20/jquery.datetimepicker.full.min.js',
 
        ]
    },
    'installable': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: