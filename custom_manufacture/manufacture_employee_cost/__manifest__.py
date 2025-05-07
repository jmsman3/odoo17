# -*- coding: utf-8 -*-

{
    'name': 'Manufacture Worcenter Practice',
    'version': '1.0.0',
    'summary': 'This is Manufacture Worcenter',
    'description': """This is the description of manufacture system""",
    'category': 'jubaer',
    'author':'Md. Jubaer Mahmud Sarker',

    'depends':['base','mail','mrp'],
    'data':[
        'security/ir.model.access.csv',  # Link to access control file
        "views/manufacture_1.xml",
    
    ],  #xml gula locate hobe
    'demo':[], #system e demo data show koranor jonno

    'installable': True,
    'application': True,   
    'auto_install': False,
    'sequence': 6,
    'license':'LGPL-3',
}



# local:8017/web/database/manager
