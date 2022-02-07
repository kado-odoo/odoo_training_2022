{
    'name': 'Real Estate',
    'category': 'Tools',
    'application' : True,
    'depends': ['base', 'website'],
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'data/estate_data.xml',
        'views/estate_property_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_templates.xml',
        'wizard/estate_wizard_views.xml',
    ],
    'license': 'LGPL-3',
}