# -*- coding: utf-8 -*-
{
    'name': "Bd Portal Inherit Users",

    'summary': """
        """,

    'description': """
        This module appends below fields to res.users and view added to user form view
        
        Inherit Fields:
        
        * department_head
        * it_department
        * admin_department
        * finance_department
        * scm_department
        
        Need to install before 'bd_portal' module installation
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/team.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
