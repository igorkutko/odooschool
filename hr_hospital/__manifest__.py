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
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/patient_card_views.xml',
        'views/doctor_views.xml',
        'views/diagnosis_views.xml',
        'views/hr_hospital_menus.xml',
    ],

    'demo': [

    ],
    'license': 'LGPL-3',

}
