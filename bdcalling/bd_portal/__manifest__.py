# -*- coding: utf-8 -*-
{
    'name': "BdCalling Portal",

    'summary': """
        Portal Features""",

    'description': """
        Portal Features
    """,

    'author': "Abdur Razzak",
    'website': "https://www.xsellencebdltd.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'hr', 'product', 'stock', 'contacts', 'portal', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/views.xml',
        # 'views/templates.xml',
        # 'views/templates/portal/base.xml',
        # 'views/templates/portal/dashboard.xml',
        # 'views/templates/portal/sales.xml',
        # 'views/templates/portal/create_sale.xml',
        # 'views/templates/portal/create_sale_status.xml',
        # 'views/templates/portal/create_new_customer.xml',
        # 'views/templates/portal/create_new_customer_status.xml',
        # 'views/templates/portal/sale_details.xml',
        # 'views/templates/portal/update_sale.xml',
        # 'views/templates/portal/requisition.xml',
        # 'views/templates/portal/requisition_status.xml',
        # 'views/templates/portal/requisition_approval.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
