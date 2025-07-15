{
    'name': 'Real Estate Advertisement',
    'version': '1.0',
    'summary': 'Basic module to manage real estate advertisements',
    'author': 'Janani',
    'category': 'Real Estate',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'Real_Estate/static/src/css/placeholder_styles.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
