# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'travel_management',
    'author': 'Salim Hossain',
    'summary': 'Travel Information',

    'category': 'jubaer',
    'depends': ['base','mail'],
    'description': "Hello",
    'data': [
        'security/ir.model.access.csv',
        'views/travel_views.xml',
        'views/customer_views.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 5,
    'license': 'LGPL-3',

}
    
