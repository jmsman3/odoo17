# -*- coding: utf-8 -*-

{
    'name': 'Foodpanda Module',
    'version': '1.0.0',
    'summary': 'This is foodpanda management system',
    'description': """This is the description of foodpanda management system""",
    'category': 'jubaer',
    'author':'Md. Jubaer Mahmud Sarker',

    'depends':['base','mail','account','web'],
    'data':[
        'security/ir.model.access.csv',  # Link to access control file
        "views/item.xml",
        "views/chef.xml",
        "views/account_move_views.xml",
        "views/cron.xml",
        "report/report_template.xml",  
        "report/report_action.xml",      
    
    ],  #xml gula locate hobe
    'demo':[], #system e demo data show koranor jonno

    'installable': True,
    'application': True,   
    'auto_install': False,
    'sequence': 5,
    'license':'LGPL-3',
}



# local:8017/web/database/manager
