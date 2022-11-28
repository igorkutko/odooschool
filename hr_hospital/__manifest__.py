{
    'name': 'hr_hospital',
    'summary': """
Hospital: human resources
    """,

    'author': 'Igor Kutko',
    'website': 'https://www.it-artel.ua',
    'category': 'hr',
    'version': '15.0.1.0.0',

    'depends': [
        'base',
    ],

    'data': [
        'security/hr_hospital_groups.xml',
        'security/hr_hospital_visit_security.xml',
        'security/ir.model.access.csv',
        'views/hr_hospital_menus.xml',
        'views/contact_person_views.xml',
        'views/disease_views.xml',
        'views/disease_type_views.xml',
        'views/diagnosis_views.xml',
        'views/doctor_schedule_views.xml',
        'views/patient_card_views.xml',
        'views/personal_doctor_history_views.xml',
        'views/research_type_views.xml',
        'views/research_views.xml',
        'views/sample_type_views.xml',
        'views/visit_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'wizard/bulk_personal_doctor_views.xml',
        'wizard/change_doctor_schedule_views.xml',
        'wizard/change_visit_views.xml',
        'wizard/disease_report_views.xml',
        'report/doctor_report_templates.xml',
        'report/doctor_report_views.xml',
        'data/disease_type_data.xml',
        'data/research_type_data.xml',
        'data/sample_type_data.xml',
        'data/research_type_modify_data.xml',
    ],

    'demo': [
        'data/contact_person_demo.xml',
        'data/doctor_demo.xml',
        'data/patient_demo.xml',
    ],
    'license': 'LGPL-3',

}
