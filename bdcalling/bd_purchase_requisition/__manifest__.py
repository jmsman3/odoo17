# -*- coding: utf-8 -*-
{
    'name': "BD Calling Purchase Requisition",

    'summary': """
        BD Calling Requisition Approval""",

    'description': """
        BD Calling Requisition Approval
    """,

    'author': "Umme Huzaifa",
    'website': "https://www.xsellencebdltd.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'stock', 'hr', 'bd_portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/purchase_requisition.xml',
        'views/purchase_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # 'images': [
    #     'static/description/icon.jpg',
    # ],
    'application': True,
}

