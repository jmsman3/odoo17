# -*- coding: utf-8 -*-
{
    'name': "BDCalling accounts report",

    'summary': """
        BDCalling accounts report Features""",

    'description': """
        BDCalling accounts report Features
    """,

    'author': "A.T.M Shamiul Bashir",
    'website': "https://www.xsellencebdltd.com/",
    'category': 'Accounts',
    'version': '17.0.1.0',
    'depends': ['base', 'account', 'account_accountant'],

    # always loaded
    'data': [
        'report/account.xml',
        'views/views.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0,
    'currency': 'EUR',
    'license': 'OPL-1',
    'contributors': [
        'A.T.M Shamiul Bashir <https://github.com/xS21ATM>',
    ],

}
