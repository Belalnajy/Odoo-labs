{
    'name': 'HMS',
    'version': '1.0',
    'author': 'belal',
    'category': 'Hospital Management System',
    'description': """
        HMS
    """,
    'depends': ['base','contacts','sale','account','purchase',],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/reports.xml',
        'reports/patient_report_template.xml',
        'views/patient.xml',
        'views/customer_view.xml',
        'views/department.xml',
        'views/doctors.xml',
        'views/menus.xml',
    ],
    'assets': {'web.assets_backend': [
        'hms/static/css/patient.css',
    ]},
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}