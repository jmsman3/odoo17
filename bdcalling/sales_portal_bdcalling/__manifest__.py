# -*- coding: utf-8 -*-
{
    'name': "Portal for BD Calling",

    'summary': "",

    'description': """
    """,

    'author': "Rayta",
    'website': "",

    'category': 'Website',
    'version': '0.1',

    'depends': ['base', 'web',
                'portal','website',
                'sale_management',
                'stock',
                'hr',
                'bd_portal',
                'bd_portal_inherit_users',
                'bd_purchase_requisition'
                ],

    'data': [
        'security/ir.model.access.csv',
        'views/base.xml',
        'views/portal.xml',
        'views/views.xml',
        'views/operation.xml',
        'views/create_sales.xml',
        'views/create_customer.xml',
        'views/dashboard.xml',
        'views/requisition_approval.xml',
        'views/requisition_status.xml',
        'views/requisition.xml',
        # 'views/sale_details.xml',
        'views/portal_employees.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'sales_portal_bdcalling/static/src/js/add_sales.js',
            'sales_portal_bdcalling/static/src/js/add_customer.js',
            'sales_portal_bdcalling/static/src/js/add_operation.js',
            'sales_portal_bdcalling/static/src/js/sales_dashboard.js',
            'sales_portal_bdcalling/static/src/js/requisition.js',

        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
