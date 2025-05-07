# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Ansil pv (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
# {
#     'name': "Facebook Messenger in Odoo Website",
#     'version': '16.0',
#     'category': 'Marketing',
#     'summary': 'Facebook Messenger. '
#                'This helps your customers to contact you using Facebook Messenger.',
#     'description': "Let's make it easier for your customers to contact you by"
#                    "using Facebook Messenger.",
#     'author': 'Cybrosys Techno Solutions',
#     'depends': ['base', 'website', 'website_sale'],
#     'company': 'Cybrosys Techno Solutions',
#     'maintainer': 'Cybrosys Techno Solutions',
#     'website': 'https://www.cybrosys.com',
#     'images': ['static/description/banner.png'],
#     'data': [
#         'views/res_config_settings_views.xml',
#         'views/fb_chatter_templates.xml',
#         'views/fb_messenger_integration_views.xml',  # Added the missing XML file for settings
#     ],
#     'license': 'AGPL-3',
#     'installable': True,
#     'application': False,
#     'auto_install': False,
#     'external_dependencies': {
#         'python': [],
#         'bin': [],
#     },
#     'assets': {
#         'web.assets_frontend': [
#             'messenger_integration/static/src/js/messenger.js',  # If you have custom JS to add
#             'messenger_integration/static/src/css/messenger.css',  # If you have custom CSS to add
#         ],
#     },
#     'support': 'support@cybrosys.com',  # Optional: Provide a support email
# }

{
    'name': "Facebook Messenger in Odoo Website",
    'version': '16.0',
    'category': 'jubaer',
    'sequence': 6,
    'summary': 'Facebook Messenger. '
               'This helps your customers to contact you using Facebook Messenger.',
    'description': "Let's make it easier for your customers to contact you by"
                   "using Facebook Messenger.",
    'author': 'Cybrosys Techno Solutions',
    'depends': ['base', 'website', 'website_sale'],
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'images': ['static/description/banner.png'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/fb_chatter_templates.xml',
        'views/fb_messenger_integration_views.xml',  # Added the missing XML file for settings
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'assets': {
        'web.assets_frontend': [
            'messenger_integration/static/src/js/messenger.js',  # If you have custom JS to add
            'messenger_integration/static/src/css/messenger.css',  # If you have custom CSS to add
        ],
    },
    'support': 'support@cybrosys.com',  # Optional: Provide a support email
}
