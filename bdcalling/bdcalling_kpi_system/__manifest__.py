# -*- coding: utf-8 -*-
{
    'name': 'KPI Bonus System',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Manage employee KPIs and calculate bonuses based on sales achievements',
    'description': """
        KPI Bonus System
        ----------------
        This module allows you to:
        * Define KPI roles, grades, and levels
        * Assign KPIs to employees
        * Record sales achievements
        * Calculate bonuses based on achievement levels
    """,
    'author': 'Rayta',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'hr', 'mail','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/kpi_config_views.xml',
        'views/emp_kpi.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}