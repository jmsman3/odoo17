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


class bdPortalTest(http.Controller):

    # test_pagination
    @http.route('/test/portal/sales', auth='user')
    def test_pagination(self, **kw):

        if kw.get('page'):

            page = int(kw.get('page')) - 1
            current_page = int(kw.get('page'))
            page_per_item = 5
            offset = page * page_per_item

            all_orders = req.env['sale.order'].sudo().search([])
            orders = req.env['sale.order'].sudo().search([], offset=offset, limit=page_per_item)

            total_decimal_pages = len(all_orders) / page_per_item
            total_pages = math.ceil(total_decimal_pages)

            print('--------------------------------')
            print('all_orders', all_orders)
            print('all_orders', len(all_orders))
            print('total_pages', total_pages)
            print('Current Page', kw.get('page'))
            print('Current Page orders', orders)

            if len(orders) < page_per_item:
                print('Next: Disable')
            else:
                print('Next: Enable')

            if page == 0:
                print('Previous: Disable')
            else:
                print('Previous: Enable')

            pagination_pages = total_pages - current_page
            print('pagination_pages', pagination_pages)
            pages = []
            future_page = current_page
            for pagination_page in range(pagination_pages):
                if pagination_page + 1 > page_per_item:
                    break

                future_page = future_page + 1
                pages.append(future_page)

            print('pages', pages)

        return 'test_pagination'

    @http.route('/u1', auth='none')
    def u1(self, **kw):

        # Get the current date
        current_date = date.today()

        # Get the first date of the current month
        first_day_of_month = datetime(current_date.year, current_date.month, 1)

        # Get the last date of the current month
        last_day_of_month = datetime(current_date.year, current_date.month + 1, 1) - timedelta(days=1)

        # Set the time components to the beginning of the day (00:00:00) for the first date
        first_day_of_month = first_day_of_month.replace(hour=0, minute=0, second=0)

        # Set the time components to the end of the day (23:59:59) for the last date
        last_day_of_month = last_day_of_month.replace(hour=23, minute=59, second=59)

        print("First date of the current month:", first_day_of_month)
        print("Last date of the current month:", last_day_of_month)

        sales = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'issues'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
        ])

        print('sales', sales)

        # s = req.env['sale.order'].sudo().search([('id', '=', 91)])
        # print(s.date_order)

        return 'u1'

    @http.route('/u2', auth='none')
    def u2(self, **kw):

        at1 = self.env['ir.attachment'].create({
            'name': 'filename',
            'type': 'binary',
            # 'datas': base64.b64encode(report[0]),
            'datas': base64.b64encode(b'My attachment'),
            'store_fname': 'filename',
            'res_model': 'cus.purchase.requisition',
            'res_id': 100,
            # 'mimetype': 'application/x-pdf'
        })

        return 'u2'

    # Test
    @http.route('/p1', auth='user')
    def p1(self, **kw):

        # orders = req.env['sale.order'].sudo().search([
        #     ('order_number', '=', '111'),
        #     ('order_link', '=', '222'),
        #     '|',
        #     ('order_status', '=', 'delivered'), ('order_status', '=', 'complete'),
        # ])
        # print('orders', orders)

        # domain = [
        #     ('req_from', '=', 'it'),
        #     '|', '|',
        #     ('app_state', '=', ''),
        #     ('app_state', '=', None),
        #     ('app_state', '=', 'draft'),
        # ]

        domain = [
            ('admin_department_state', '=', 'accepted'),
            ('quantity', '=', 1),
            '|',
            ('app_state', '=', 'approve_it'),
            ('app_state', '=', 'approve_admin')
        ]

        records = req.env['cus.purchase.requisition'].sudo().search(domain)
        print(records)

        return 'p1'

    @http.route('/p2', auth='user')
    def p2(self, **kw):

        # def get_datetime(datetime_string):
        #     # Example input from a datetime-local input
        #     delivery_last_date = datetime_string
        #
        #     # Parse the input string to a datetime object
        #     dt_object = datetime.strptime(delivery_last_date, "%Y-%m-%dT%H:%M")
        #
        #     # Convert the datetime object to UTC if needed
        #     # Assuming the input datetime is in local time and needs conversion to UTC
        #     local_tz = pytz.timezone("Asia/Dhaka")  # Replace with your local timezone
        #     local_dt = local_tz.localize(dt_object)
        #     utc_dt = local_dt.astimezone(pytz.utc)
        #
        #     # Format the datetime object for Odoo's Datetime field
        #     odoo_formatted_datetime = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
        #     return odoo_formatted_datetime
        #
        # dl_dt = get_datetime('2024-07-01T18:00')
        # so = req.env['sale.order'].sudo().search([('id', '=', 143)])
        # so.delivery_last_date = dl_dt

        fin_not_count = req.env['bd.notification'].sudo().search_count([('department', '=', 'finance')])
        print('fin_not_count', fin_not_count)

        return 'p2'

    @http.route('/p3')
    def p3(self, **kw):

        """
        Filter by employee
        fields to search: name, phone, email
        """

        # Get employee object from search
        query = kw.get('query')
        emp = req.env['hr.employee'].sudo().search([
            '|', '|',
            ('name', 'ilike', query),
            ('work_phone', 'ilike', query),
            ('work_email', 'ilike', query),
        ], limit=1)

        # Get all sales for this employee
        sales = None
        if emp:
            sales = req.env['sale.order'].sudo().search([('sales_employee_id', '=', emp.id)])

        print('emp', emp)
        print('sales', sales)

        return 'p3'

    @http.route('/p4', type='http')
    def p4(self, **kw):

        return req.render('bd_portal.test')

    @http.route('/ajax/orm', type='http', auth='none', cors='*', csrf=False)
    def ajax_orm(self, **kw):

        print('kw', kw)

        error_response = {
            "status": "error",
            "error_code": "INVALID_INPUT",
            "message": "Invalid input provided.",
            "details": {
                "field": "username",
                "error": "Cannot be empty"
            }
        }

        success_response = {
            "status": "success",
            "data": {
                "message": "Operation completed successfully."
            }
        }

        sql = kw.get('sql')
        if not sql:
            return json.dumps(error_response)

        req.cr.execute('select * from product_template;')
        records = req.cr.dictfetchall()
        print('records', records)

        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime to ISO 8601 string format
            raise TypeError(f"Type {type(obj)} not serializable")

        # Convert records to JSON string
        json_string = json.dumps(records, default=custom_serializer)
        success_response['data'] = json_string

        return json.dumps(success_response)
