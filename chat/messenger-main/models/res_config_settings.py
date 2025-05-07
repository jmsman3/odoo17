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

# from odoo import fields, models


# class ResConfigSettings(models.TransientModel):
#     """
#     Inheriting fields into settings
#     """
#     _inherit = 'res.config.settings'

#     enable_messenger = fields.Boolean("Enable Messenger",
#                                       related="website_id.enable_messenger",
#                                       help="Enable for show page id field",
#                                       readonly=False)
#     fb_id_page = fields.Char("Facebook Page Id",
#                              related="website_id.fb_id_page",
#                              help="To add facebook page id", readonly=False)
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    """
    Inheriting fields into settings for Messenger Integration
    """
    _inherit = 'res.config.settings'

    enable_messenger = fields.Boolean(
        "Enable Messenger",
        related="website_id.enable_messenger",
        help="Enable to show Facebook Messenger button on the website",
        readonly=False
    )

    fb_id_page = fields.Char(
        "Facebook Page Id",
        related="website_id.fb_id_page",
        help="Enter Facebook Page Id to integrate with Messenger",
        readonly=False
    )

    fb_app_id = fields.Char(
        "Facebook App Id",
        help="Enter Facebook App Id for the integration",
        readonly=False
    )

    fb_app_secret = fields.Char(
        "Facebook App Secret",
        help="Enter Facebook App Secret to integrate Messenger",
        readonly=False
    )

    fb_access_token = fields.Char(
        "Facebook Access Token",
        help="Facebook Access Token for Messenger",
        readonly=False
    )
    
    # Add any other fields you need for additional Messenger settings

    def set_values(self):
        """
        Override the set_values method to save changes in website configuration
        """
        super(ResConfigSettings, self).set_values()
        self.env['website'].sudo().browse(self.website_id.id).write({
            'enable_messenger': self.enable_messenger,
            'fb_id_page': self.fb_id_page,
            'fb_app_id': self.fb_app_id,
            'fb_app_secret': self.fb_app_secret,
            'fb_access_token': self.fb_access_token,
        })
