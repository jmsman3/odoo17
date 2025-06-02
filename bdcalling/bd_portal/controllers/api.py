# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request, request as req
from odoo import Command
from datetime import datetime, time, date, timedelta
import math
import base64
import pytz


def get_partner():
    user_id = req.env.user.id
    res_user = req.env['res.users'].sudo().search([('id', '=', user_id)], limit=1)

    if res_user:
        return res_user.partner_id
    else:
        return None


class bdPortalApi(http.Controller):
    @http.route('/api/v1/products', type='json', auth="user", cors="*", methods=['GET', 'POST', 'OPTIONS'])
    def api_products(self, **kw):
        products = [
            {
                'name': 'Samsung M01',
                'price': 12000,
            },
            {
                'name': 'Mug',
                'price': 50,
            }

        ]

        return products

    @http.route('/api/v1/public/get_categories', type='json', auth="none", cors="*", methods=['GET', 'POST', 'OPTIONS'])
    def public_get_categories(self, **kw):
        categories = [
            {
                'name': 'Smartphone',
            },
            {
                'name': 'Electronics',
            }

        ]

        return categories
