

{
    'name': "School Management Demo",
    'category': 'Base',
    'version': '16.0.1.0',
    'sequence': 5,
    'summary': """add new model for school management """,
    'description': """ This plugin will help to add new model school management """,

    'author': 'Leap4Logic Solutions Private Limited',
    'website': 'https://leap4logic.com/',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_student.xml',
        'data/sequence_result.xml',
        'wizard/create_student_view.xml',
        'views/main_menu_view.xml',
        'views/leap_student_student_views.xml',
        'views/leap_class_class_views.xml',
        'views/leap_subject_subject_views.xml',
        'views/leap_result_result_views.xml',
    ],
    # Order of placing file name in data is security, data, view, wizard, report
    'installable': True,
    'application': True,
}

