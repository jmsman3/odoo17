# -*- coding: utf-8 -*-
{
    'name': 'BDCalling Reconciliation Extend',
    'summary': """BDCalling Reconciliation Extend.""",
    'description': """
BDCalling Reconciliation Extend
========
Something about the App.
    """,
    'version': '17.0.1.0',
    'author': 'A.T.M Shamiul Bashir',
    'website': 'http://www.xsellencebdltd.com',
    'category': 'Tools',
    'sequence': 1,
    'depends': [
        'base',
        'account',
        'account_accountant',
    ],
    'data': [
        'views/bank_statement.xml',
        'views/account_account.xml',
    ],
    'external_dependencies': {
        'python': [
            'werkzeug',
        ],
    },

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
