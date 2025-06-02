# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request, request as req
from odoo import Command
from datetime import datetime, time, date, timedelta
import math
from werkzeug.utils import redirect
import base64
from collections import defaultdict
import pytz
from odoo import models, fields, api
import calendar


def get_partner():
    user_id = req.env.user.id
    res_user = req.env['res.users'].sudo().search(
        [('id', '=', user_id)], limit=1)

    if res_user:
        return res_user.partner_id
    else:
        return None


class BdPortal(http.Controller):

    @http.route('/ajax/check_unique_order', type='http', auth='user', cors='*', csrf=False)
    def ajax_check_unique_order(self, **kw):

        order_number = kw.get('order_number')
        print('order_number444', order_number)

        if not order_number:
            return 'error'

        order = req.env['sale.order'].sudo().search(
            [('order_number', '=', order_number)])
        print('order33', order)
        if order:
            return 'exist'

        return 'success'

    @http.route('/ajax/create_new_client', type='http', auth='user', cors='*', csrf=False)
    def create_new_client(self, **kw):

        error = False
        error_response = {
            "status": "error",
            "error": {
                "code": 404,
                "message": "Error message"
            }
        }

        success_response = {
            "status": "success",
            "data": {
                "client": {}
            },
            "message": "New Client Created successfully."
        }

        # Validate
        client_user_name = kw.get('client_user_name')
        mp_customer_fullname = kw.get('mp_customer_fullname')
        street = kw.get('street')
        city = kw.get('city')
        _zip = kw.get('zip')
        country_id = kw.get('country_id')
        phone = kw.get('phone')
        email = kw.get('email')
        website = kw.get('website')

        # If client not posted / pass
        if not client_user_name:
            error = True
            error_response['error']['message'] = 'Client id not passed'

        # Check if client already exists
        client = req.env['res.partner'].sudo().search([
            ('is_mp_customer', '=', True),
            ('name', '=', client_user_name),
        ])
        if client:
            error = True
            error_response['error'][
                'message'] = f'Already have a client <b>{client.name}</b>. Please try a different one'

        # Error response
        if error:
            return json.dumps(error_response)

        # Create new client
        client_values = {
            'is_mp_customer': True,
            'name': client_user_name,
            'mp_customer_fullname': mp_customer_fullname,
            'street': street,
            'city': city,
            'zip': _zip,
            'country_id': country_id,
            'phone': phone,
            'email': email,
            'website': website,
        }

        new_client = req.env['res.partner'].sudo().sudo().create(client_values)

        if not new_client:
            error = True
            error_response['error']['message'] = 'Client not created'

        success_response['message'] = f'Successfully Client <b>{new_client.name}</b> Created'

        my_client = {
            "id": new_client.id,
            "client_user_name": new_client.name,
            "name": "yyy",
            "email": new_client.email,
            "phone": new_client.phone,
            "mp_customer_fullname": new_client.mp_customer_fullname
        }
        success_response['data']['client'] = my_client

        # Success response
        return json.dumps(success_response)

    """
    Portal Dashboard
    Monthly basis data will show
    """

    @http.route('/portal/dashboard', auth='user')
    def portal_dashboard(self, **kw):
        # Global Variables
        user_id = req.env.user

        # Get the current date
        current_date = date.today()

        # Get the first date of the current month
        first_day_of_month = datetime(current_date.year, current_date.month, 1)

        # Get the current year and month --------------
        a_now = datetime.now()
        a_year = a_now.year
        a_month = a_now.month

        # Get the last day of the current month
        last_day = calendar.monthrange(a_year, a_month)[1]

        print(f"The last day of the current month is: {last_day}")
        # Get the current year and month --------------

        # Get the last date of the current month
        if last_day == 31:
            last_day_of_month = datetime(
                current_date.year, current_date.month, 1) - timedelta(days=1)
            print('last_day_of_month', last_day_of_month)
        else:
            last_day_of_month = datetime(
                current_date.year, current_date.month + 1, 1) - timedelta(days=1)
            print('last_day_of_month', last_day_of_month)

        # Set the time components to the beginning of the day (00:00:00) for the first date
        first_day_of_month = first_day_of_month.replace(
            hour=0, minute=0, second=0)

        # Set the time components to the end of the day (23:59:59) for the last date
        last_day_of_month = last_day_of_month.replace(
            hour=23, minute=59, second=59)

        total_order = req.env['sale.order'].sudo().search([
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('company_id', '=', user_id.company_id.id),
        ])

        total_wip = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'wip'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
        ])

        total_completed = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'complete'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
        ])

        total_canceled = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'cancelled'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
        ])

        total_nra = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'nra'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
        ])

        total_revisions = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'revisions'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
        ])

        """
        Best Sales Performer
        best_sales_performer
        """
        sales = req.env['sale.order'].sudo().search([
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('order_status', '!=', ''),
            ('order_status', '!=', 'cancelled'),
        ])

        best_sales = []
        for sale in sales:
            best_sale = [sale.sales_employee_id.id, sale.amount_total]
            best_sales.append(best_sale)

        # Initialize a dictionary to store the total sales amount for each employee ID
        sales_totals = defaultdict(float)

        # Calculate the total sales amount for each employee
        for employee in best_sales:
            employee_id, amount = employee
            sales_totals[employee_id] += amount

        # Find the employee ID with the highest total sales amount
        best_employee_id = None
        try:
            best_employee_id = max(sales_totals, key=sales_totals.get)
        except ValueError:
            pass

        best_sale_performer = req.env['hr.employee'].sudo().search(
            [('id', '=', best_employee_id)])

        """
        Best Delivery Performer
        best_delivery_performer
        """
        sales_delivered = req.env['sale.order'].sudo().search([
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            '|',
            ('order_status', '=', 'delivered'), ('order_status', '=', 'complete'),
        ])

        best_sales_delivered = []
        for sale_d in sales_delivered:
            best_sale_d = [sale_d.delivered_team_id.id, sale_d.amount_total]
            best_sales_delivered.append(best_sale_d)

        # Initialize a dictionary to store the total sales amount for each employee ID
        sales_totals_d = defaultdict(float)

        # Calculate the total sales amount for each employee
        for team in best_sales_delivered:
            team_id, amount = team
            sales_totals_d[team_id] += amount

        # Find the employee ID with the highest total sales amount
        best_team_id = None
        try:
            best_team_id = max(sales_totals_d, key=sales_totals_d.get)
        except ValueError:
            pass

        best_delivery_team_id = req.env['bd.team'].sudo().search(
            [('id', '=', best_team_id)])

        """Purchase Requisition"""
        total_pr_count = req.env['cus.purchase.requisition'].sudo().search_count([
        ])
        print('total_pr_count:', total_pr_count)

        total_dh_acc_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('department_head_state', '=', 'accepted')
        ])
        print('total_dh_acc_count:', total_dh_acc_count)

        total_it_acc_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('it_department_state', '=', 'accepted')
        ])
        print('total_it_acc_count:', total_it_acc_count)

        total_ad_acc_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('admin_department_state', '=', 'accepted')
        ])
        print('total_ad_acc_count:', total_ad_acc_count)

        total_scm_acc_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('scm_department_state', '=', 'accepted')
        ])
        print('total_scm_acc_count:', total_scm_acc_count)

        total_fin_acc_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('finance_department_state', '=', 'accepted')
        ])
        print('total_fin_acc_count:', total_fin_acc_count)

        total_ceo_acc_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('ceo_state', '=', 'accepted')
        ])
        print('total_ceo_acc_count:', total_ceo_acc_count)

        """Pending"""
        print('Pending---------------------')
        total_dh_pen_count = req.env['cus.purchase.requisition'].sudo().search_count([
            '|',
            ('app_state', '=', 'draft'),
            ('app_state', '=', 'submit')
        ])
        print('total_dh_pen_count:', total_dh_pen_count)

        total_it_pen_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('req_from', '=', 'it'),
            ('app_state', '=', 'approve_dh'),
        ])
        print('total_it_pen_count:', total_it_pen_count)

        total_ad_pen_count = req.env['cus.purchase.requisition'].sudo().search_count([
            '|',
            ('app_state', '=', 'approve_dh'),
            ('app_state', '=', 'approve_it'),
        ])
        print('total_ad_pen_count:', total_ad_pen_count)

        total_scm_pen_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('app_state', '=', 'approve_admin'),
        ])
        print('total_scm_pen_count:', total_scm_pen_count)

        total_fin_pen_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('app_state', '=', 'approve_scm'),
        ])
        print('total_fin_pen_count:', total_fin_pen_count)

        total_ceo_pen_count = req.env['cus.purchase.requisition'].sudo().search_count([
            ('app_state', '=', 'approve_finance'),
        ])
        print('total_ceo_pen_count:', total_ceo_pen_count)

        """End Purchase Requisition"""

        purchase_access = False
        if user_id.department_head or user_id.it_department or user_id.admin_department or user_id.scm_department or user_id.finance_department or user_id.is_ceo:
            purchase_access = True

        print('purchase_access', purchase_access)

        # sale_access = ''

        return req.render('bd_portal.dashboard', {
            'total_order': total_order,
            'total_wip': total_wip,
            'total_completed': total_completed,
            'total_canceled': total_canceled,
            'total_nra': total_nra,
            'total_revisions': total_revisions,
            'best_sale_performer': best_sale_performer,
            'best_delivery_team_id': best_delivery_team_id,

            # Purchase Requisition
            'total_pr_count': total_pr_count,
            'total_dh_acc_count': total_dh_acc_count,
            'total_it_acc_count': total_it_acc_count,
            'total_ad_acc_count': total_ad_acc_count,
            'total_scm_acc_count': total_scm_acc_count,
            'total_fin_acc_count': total_fin_acc_count,
            'total_ceo_acc_count': total_ceo_acc_count,

            # Pending Purchase Requisition
            'total_dh_pen_count': total_dh_pen_count,
            'total_it_pen_count': total_it_pen_count,
            'total_ad_pen_count': total_ad_pen_count,
            'total_scm_pen_count': total_scm_pen_count,
            'total_fin_pen_count': total_fin_pen_count,
            'total_ceo_pen_count': total_ceo_pen_count,

            'purchase_access': purchase_access
        })

    # View all sales with pagination
    @http.route('/portal/sales', auth='user')
    def portal_sales(self, **kw):

        filter_order_id = kw.get('filter_order_id')
        is_filter = False
        user_id = req.env.user

        print('user_id:', user_id)
        print('user_id:is_project_manager', user_id.is_project_manager)

        emp = req.env['hr.employee'].sudo().search(
            [('user_id2', '=', user_id.id)])
        print('emp', emp.name)

        # Filter by order number (single)
        if filter_order_id:
            orders = req.env['sale.order'].sudo().search(
                [('order_number', '=', filter_order_id)])
            is_filter = True

            return req.render('bd_portal.sales', {
                'kw': kw,
                'orders': orders,
                'filter_order_id': filter_order_id,
                'is_filter': is_filter,
                'user_id': user_id,
            })
            # End filter by order number

        else:
            previous = 'enable'
            _next = 'enable'
            is_jumper_page = False
            jumper_page = 0

            current_page = 1
            if kw.get('page'):
                current_page = int(kw.get('page'))

            page = current_page - 1
            page_per_item = 10
            offset = page * page_per_item

            """
            filter_order_status
            """
            total_orders_domain = []
            if kw.get('filter_order_status'):
                filter_order_status = kw.get('filter_order_status')
                total_orders_domain.append(
                    ('order_status', '=', filter_order_status))
                is_filter = True

                if not user_id.is_project_manager:

                    emp = req.env['hr.employee'].sudo().search(
                        [('user_id2', '=', user_id.id)])
                    barcode = emp.barcode if emp else None

                    if barcode:
                        total_orders_domain.append(
                            ('employee_id_barcode', '=', barcode))

            print('total_orders_domain', total_orders_domain)
            total_orders = req.env['sale.order'].sudo(
            ).search_count(total_orders_domain)

            """
            filter_order_status
            For sale.order objects
            """
            orders_domain = []
            if not emp.is_all_sale:
                orders_domain.append(('create_uid', '=', user_id.id))

            if kw.get('filter_order_status'):

                filter_order_status = kw.get('filter_order_status')
                orders_domain.append(
                    ('order_status', '=', filter_order_status))
                is_filter = True

                if not user_id.is_project_manager:

                    emp = req.env['hr.employee'].sudo().search(
                        [('user_id2', '=', user_id.id)])
                    barcode = emp.barcode if emp else None

                    if barcode:
                        orders_domain.append(
                            ('employee_id_barcode', '=', barcode))

            """
            Filter updates
            """
            if kw.get('f_sales_employee_id'):
                f_sales_employee_id = kw.get('f_sales_employee_id')
                orders_domain.append(
                    ('sales_employee_id', '=', int(f_sales_employee_id)))
                is_filter = True

            if kw.get('f_platform_source_id'):
                f_platform_source_id = kw.get('f_platform_source_id')
                orders_domain.append(
                    ('platform_source_id', '=', int(f_platform_source_id)))
                is_filter = True

            if kw.get('f_order_source_id'):
                f_order_source_id = kw.get('f_order_source_id')
                orders_domain.append(
                    ('order_source_id', '=', int(f_order_source_id)))
                is_filter = True

            if kw.get('f_profile_id'):
                f_profile_id = kw.get('f_profile_id')
                orders_domain.append(('profile_id', '=', int(f_profile_id)))
                is_filter = True

            if kw.get('f_client_user_id'):
                f_client_user_id = kw.get('f_client_user_id')
                orders_domain.append(
                    ('client_user_id', '=', int(f_client_user_id)))
                is_filter = True

            if kw.get('f_order_status'):
                f_order_status = kw.get('f_order_status')
                orders_domain.append(('order_status', '=', f_order_status))
                is_filter = True

            if kw.get('f_order_id'):
                f_order_id = kw.get('f_order_id')
                orders_domain.append(('order_number', '=', f_order_id))
                is_filter = True

            """
            End Filter updates
            """

            # Append domain for employee
            # if not user_id.is_project_manager:
            #
            #     emp = req.env['hr.employee'].sudo().search([('user_id2', '=', user_id.id)])
            #     barcode = emp.barcode if emp else None
            #
            #     if barcode:
            #         orders_domain.append(('employee_id_barcode', '=', barcode))

            # Later added: To solve project manager showing all sales
            emp = req.env['hr.employee'].sudo().search(
                [('user_id2', '=', user_id.id)])
            barcode = emp.barcode if emp else None

            if barcode:
                orders_domain.append(('employee_id_barcode', '=', barcode))
            # End later added

            orders = req.env['sale.order'].sudo().search(
                orders_domain, offset=offset, limit=page_per_item)
            print('orders_domain', orders_domain)
            print('orders', orders)

            total_decimal_pages = total_orders / page_per_item
            total_pages = math.ceil(total_decimal_pages)

            if len(orders) < page_per_item:
                _next = 'disable'

            else:
                _next = 'enable'

            if page == 0:
                previous = 'disable'

            else:
                previous = 'enable'

            pagination_pages = total_pages - current_page
            pages = []
            future_page = current_page
            for pagination_page in range(pagination_pages):
                if pagination_page + 1 > page_per_item:
                    break

                future_page = future_page + 1
                pages.append(future_page)

            # print('pages', pages)

            if pages:
                jumper_page = pages[-1] + 5
                is_jumper_page = False
                # print('jumper_page', jumper_page)
                a_a = page_per_item * jumper_page
                b_b = a_a - page_per_item

                # print('a_a', a_a)
                # print('b_b', b_b)

                if b_b < total_orders:
                    # print('jumper_page available')
                    is_jumper_page = True

            url_params = ''
            if kw.get('filter_order_status'):
                url_params = url_params + \
                    f'&filter_order_status={kw.get("filter_order_status")}'

            return req.render('bd_portal.sales', {
                'kw': kw,
                'orders': orders,
                'page_per_item': page_per_item,
                'previous': previous,
                'previous_page': current_page - 1,
                '_next': _next,
                'next_page': current_page + 1,
                'pages': pages,
                'current_page': current_page,
                'is_jumper_page': is_jumper_page,
                'jumper_page': jumper_page,
                'filter_order_id': filter_order_id,
                'url_params': url_params,
                'is_filter': is_filter,
                'user_id': user_id,
            })

    # Create sales from portal
    @http.route('/portal/sales/create', auth='user')
    def portal_sales_create(self, **kw):
        pt = get_partner()
        if not pt:
            return 'Partner not found'

        env_user = req.env.user

        if env_user and not env_user.can_create_sale:
            return 'Sorry, You have no permission to create sale'

        # Service types
        service_types = req.env['product.template'].sudo().search([
            ('portal_available', '=', True),
            ('company_id', '=', req.env.company.id),
        ])

        user_id = req.env.user.id
        print('user_id', user_id)

        company_id = req.env.company
        print('company_id:', company_id)

        # profile_fiverr = req.env['bd.profile'].sudo().search([('platform_source', '=', 'fiverr')])
        # profile_upwork = req.env['bd.profile'].sudo().search([('platform_source', '=', 'upwork')])
        # profile_pph = req.env['bd.profile'].sudo().search([('platform_source', '=', 'pph')])
        # print('profile_fiverr', profile_fiverr)
        # print('profile_upwork', profile_upwork)
        # print('profile_pph', profile_pph)
        #
        # profiles = {
        #     'fiverr': None,
        #     'upwork': None,
        #     'pph': None,
        # }
        #
        # pf_items = []
        # for pf in profile_fiverr:
        #     item = {
        #         'id': pf.id,
        #         'name': pf.name,
        #     }
        #     pf_items.append(item)
        #
        # profiles['fiverr'] = pf_items
        #
        # upwork_items = []
        # for upwork in profile_upwork:
        #     item = {
        #         'id': upwork.id,
        #         'name': upwork.name,
        #     }
        #     upwork_items.append(item)
        #
        # pph_items = []
        # for pph in profile_pph:
        #     item = {
        #         'id': pph.id,
        #         'name': pph.name,
        #     }
        #     pph_items.append(item)

        # profiles['fiverr'] = pf_items
        # profiles['upwork'] = upwork_items
        # profiles['pph'] = pph_items
        #
        # json_profiles = json.dumps(profiles)
        # print('json_profiles', json_profiles)

        platform_sources = req.env['bd.platform_source'].sudo().search([])

        all_profiles = []
        profiles = req.env['bd.profile'].sudo().search(
            [('company_id', '=', company_id.id)])

        for profile in profiles:
            profile_value = {
                'platform_source_id': profile.platform_source_id.id if profile.platform_source_id else None,
                'platform_source_name': profile.platform_source_id.name if profile.platform_source_id else '',
                'name': profile.name,
                'id': profile.id,
                'company_id': company_id.id,
            }

            all_profiles.append(profile_value)

        json_all_profiles = json.dumps(all_profiles)
        print('json_all_profiles', json_all_profiles)

        # ----

        # Clients
        client_user_ids = req.env['res.partner'].sudo().search([
            ('is_mp_customer', '=', True),
            ('name', '!=', ''),
        ])
        clients = []
        for client in client_user_ids:
            _client = {
                'id': client.id,
                'client_user_name': client.name,
                'name': client.name,
                'email': client.email,
                'phone': client.phone,
                'mp_customer_fullname': client.mp_customer_fullname,
            }
            clients.append(_client)
        js_clients = json.dumps(clients)

        # Employee Details
        employee_id = req.env['hr.employee'].sudo().search(
            [('user_id2', '=', user_id)])
        if not employee_id:
            return 'Employee not found for this user'

        # All Companies
        # companies = req.env['res.company'].sudo().search([('active', '=', True)])
        # print('companies', companies)

        # Sales Employee Details
        employees_ids = req.env['hr.employee'].sudo().search(
            [('barcode', '!=', False)])
        employees = []
        for employee in employees_ids:
            _employee = {
                'id': employee.id,
                'name': employee.name,
                'barcode': employee.barcode,
                'company_name': employee.company_id.name if employee.company_id else None,
            }
            employees.append(_employee)
        js_employees = json.dumps(employees)

        # Server data
        # Server data
        server_data = {
            'service_types': None,
        }

        # Service types
        service_types_list = []
        for st in service_types:
            vals = {
                'id': st.id,
                'unit_price': st.list_price,
            }
            service_types_list.append(vals)

        server_data['service_types'] = service_types_list

        # Employee Information
        employee = {
            'id': employee_id.id,
            'barcode': employee_id.barcode if employee_id.barcode else '',
            'name': employee_id.name,
        }

        server_data['employee'] = employee

        # Make json
        js_server_data = json.dumps(server_data)

        # Start a session
        req.session['session_create_sale'] = True

        # Project Information
        is_project_manager = False
        if env_user.department_head or env_user.it_department:
            is_project_manager = True

        order_sources = req.env['bd.order_source'].sudo().search([])

        # Crm tags
        tags = req.env['crm.tag'].sudo().search([])

        return req.render('bd_portal.create_sale', {
            'service_types': service_types,
            # 'is_portal_manager': is_portal_manager,
            'user_id': user_id,
            'company_id': company_id,
            # 'json_profiles': json_profiles,
            'client_user_ids': client_user_ids,
            'js_clients': js_clients,
            'employee_id': employee_id,
            'js_employees': js_employees,
            'js_server_data': js_server_data,
            'is_project_manager': is_project_manager,
            'env_user': env_user,
            'order_sources': order_sources,
            'platform_sources': platform_sources,
            'json_all_profiles': json_all_profiles,
            'tags': tags,
        })

    # Create sales status
    @http.route('/portal/sales/create/status', auth='user', csrf=False)
    def portal_sales_create_status(self, **kw):

        def get_datetime(datetime_string):
            # Example input from a datetime-local input
            delivery_last_date = datetime_string

            # Parse the input string to a datetime object
            dt_object = datetime.strptime(delivery_last_date, "%Y-%m-%dT%H:%M")

            # Convert the datetime object to UTC if needed
            # Assuming the input datetime is in local time and needs conversion to UTC
            # Replace with your local timezone
            local_tz = pytz.timezone("Asia/Dhaka")
            local_dt = local_tz.localize(dt_object)
            utc_dt = local_dt.astimezone(pytz.utc)

            # Format the datetime object for Odoo's Datetime field
            odoo_formatted_datetime = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
            return odoo_formatted_datetime

        if not req.session.get('session_create_sale'):
            print('/portal/sales/create')
            return redirect('/portal/sales/create')

        print('client_user_id', kw.get('client_user_id'))
        if not kw.get('client_user_id'):
            print('client_user_id')
            return 'Client User ID (Customer) not found'

        req.session.pop('session_create_sale', None)
        sale_order_values = {
            # Employee
            'employee_id': kw.get('employee_id'),
            # Sales Employee
            'sales_employee_id': kw.get('sales_employee_id'),
            # Sale Order
            'platform_source_id': kw.get('platform_source_id'),
            'order_source_id': kw.get('order_source_id'),
            'profile_id': kw.get('profile_id'),
            'client_user_id': kw.get('client_user_id') if kw.get('client_user_id') else None,
            'order_number': kw.get('order_number'),
            'order_link': kw.get('order_link'),
            'instruction_sheet_link': kw.get('instruction_sheet_link'),
            'service_type_id': kw.get('service_type_id'),
            'incoming_date': kw.get('incoming_date'),
            'delivery_last_date': get_datetime(kw.get('delivery_last_date')),

            'amount': kw.get('amount'),
            'percentage': kw.get('percentage'),
            'charges_amount': kw.get('charges_amount'),
            'delivery_amount': kw.get('delivery_amount'),

            'special_remarks': kw.get('special_remarks'),

            'crm_tag_ids': [(6, 0, [int(tag) for tag in kw.get('tags', [])])] if kw.get('tags') else False,
            'partner_id': int(kw.get('client_user_id')),
            'order_status': kw.get('order_status'),
        }
        # Operation employee
        if kw.get('operation_employee_id'):
            sale_order_values['operation_employee_id'] = kw.get(
                'operation_employee_id')
            sale_order_values['assigned_team_id'] = kw.get('assigned_team_id')
            sale_order_values['delivered_team_id'] = kw.get(
                'delivered_team_id')
            sale_order_values['order_status'] = kw.get('order_status')
            sale_order_values['teams_delivery_date'] = kw.get(
                'teams_delivery_date')

        if kw.get('service_type_id'):
            service_tmpl_id = req.env['product.template'].sudo().search(
                [('id', '=', int(kw.get('service_type_id')))])
            if service_tmpl_id:
                service_product_id = req.env['product.product'].sudo().search(
                    [('product_tmpl_id', '=', service_tmpl_id.id)])

                if service_product_id:
                    sale_order_values['order_line'] = [Command.create({
                        'product_id': service_product_id.id,
                        'product_uom_qty': 1,
                        # 'product_uom': self.product_a.uom_id.id,
                        'price_unit': float(kw.get('delivery_amount')) if kw.get('delivery_amount') else 0,
                        'tax_id': False,
                    })]

        new_sale = req.env['sale.order'].sudo().create(sale_order_values)
        if new_sale:
            new_sale.sudo().action_confirm()
            print('Order created')
        else:
            print('Order not created')

        return req.render('bd_portal.create_sale_status', {
            'order': new_sale,
        })

    """
    Create New Customer
    """

    @http.route('/portal/sales/create_new_customer', auth='user')
    def create_new_customer(self, **kw):
        # pt = get_partner()
        # if not pt:
        #     return 'Partner not found'

        req.session['session_create_new_customer'] = True

        return req.render('bd_portal.create_new_customer', {
            'kw': kw,
        })

    @http.route('/portal/sales/create_new_customer/status', auth='user', csrf=False)
    def create_new_customer_status(self, **kw):

        session_create_new_customer = req.session.get(
            'session_create_new_customer')
        if not session_create_new_customer:
            return redirect('/portal/sales/create_new_customer')

        req.session.pop('session_create_new_customer', None)

        # Create customer
        customer_values = kw

        if 'image_1920' in kw:
            image_1920_file = kw.get('image_1920')
            customer_values['image_1920'] = base64.b64encode(
                image_1920_file.read())

        customer_values['is_mp_customer'] = True

        new_customer = req.env['res.partner'].sudo().create(customer_values)

        alert_info = None
        alert_danger = None

        if new_customer:
            alert_info = f'Customer {new_customer.name} created successfully'
        else:
            alert_danger = f'Create New Customer Failed'

        return req.render('bd_portal.create_new_customer_status', {
            'kw': kw,
            'new_customer': new_customer,
            'alert_info': alert_info,
            'alert_danger': alert_danger,
        })

    """
    View sale order details in edit mode
    """

    @http.route('/portal/sales/details', auth='user')
    def portal_sales_details(self, **kw):
        pt = get_partner()
        if not pt:
            return 'Partner not found'

        is_portal_manager = pt.operation_manager

        order_id = kw.get('order_id')
        if not order_id:
            return 'order_id not found'

        order_id = int(order_id)

        order = req.env['sale.order'].sudo().search([('id', '=', order_id)])
        print('order', order)
        if not order:
            return 'Order object not found'

        # Service types
        service_types = req.env['product.template'].sudo().search(
            [('portal_available', '=', True)])

        print('charges_amount', order.charges_amount)
        f_charges_amount = f"{order.charges_amount:.2f}"
        f_delivery_amount = f"{order.delivery_amount:.2f}"

        user_id = req.env.user.id
        print('user_id', user_id)

        company_id = req.env.company
        print('company_id', company_id)

        client_user_ids = req.env['res.partner'].sudo().search([])

        # Project Information
        is_project_manager = False
        env_user = req.env.user

        if env_user.department_head or env_user.it_department:
            is_project_manager = True

        # Sales Employee Details
        employees_ids = req.env['hr.employee'].sudo().search(
            [('barcode', '!=', False)])
        employees = []
        for employee in employees_ids:
            _employee = {
                'id': employee.id,
                'name': employee.name,
                'barcode': employee.barcode,
                'company_name': employee.company_id.name if employee.company_id else None,
            }
            employees.append(_employee)
        js_employees = json.dumps(employees)

        # Employee Details
        employee_id = req.env['hr.employee'].sudo().search(
            [('user_id2', '=', user_id)])
        if not employee_id:
            return 'Employee not found for this user'

        service_types = req.env['product.template'].sudo().search(
            [('portal_available', '=', True)])

        # Server data
        server_data = {
            'service_types': None,
        }

        # Service types
        service_types_list = []
        for st in service_types:
            vals = {
                'id': st.id,
                'unit_price': st.list_price,
            }
            service_types_list.append(vals)

        server_data['service_types'] = service_types_list

        # Employee Information
        employee = {
            'id': employee_id.id,
            'barcode': employee_id.barcode if employee_id.barcode else '',
            'name': employee_id.name,
        }

        server_data['employee'] = employee

        # Make json
        js_server_data = json.dumps(server_data)

        delivery_last_date = order.delivery_last_date
        dld_plus_6_hour = delivery_last_date + \
            timedelta(hours=6)  # Need to fix

        """Clients"""
        client_user_ids = req.env['res.partner'].sudo().search([
            ('is_mp_customer', '=', True),
            ('name', '!=', ''),
        ])
        clients = []
        for client in client_user_ids:
            _client = {
                'id': client.id,
                'client_user_name': client.name,
                'name': client.name,
                'email': client.email,
                'phone': client.phone,
                'mp_customer_fullname': client.mp_customer_fullname,
            }
            clients.append(_client)
        js_clients = json.dumps(clients)
        """End Clients"""

        """
        platform_sources and profiles
        """
        platform_sources = req.env['bd.platform_source'].sudo().search([])

        all_profiles = []
        profiles = req.env['bd.profile'].sudo().search(
            [('company_id', '=', company_id.id)])

        for profile in profiles:
            profile_value = {
                'platform_source_id': profile.platform_source_id.id if profile.platform_source_id else None,
                'platform_source_name': profile.platform_source_id.name if profile.platform_source_id else '',
                'name': profile.name,
                'id': profile.id,
                'company_id': company_id.id,
            }

            all_profiles.append(profile_value)

        json_all_profiles = json.dumps(all_profiles)
        print('json_all_profiles', json_all_profiles)
        """
        End platform_sources and profiles
        """

        # Employee Details
        employee_id = req.env['hr.employee'].sudo().search(
            [('user_id2', '=', user_id)])
        if not employee_id:
            return 'Employee not found for this user'

        return req.render('bd_portal.sale_details', {
            'order': order,
            'service_types': service_types,
            'f_charges_amount': f_charges_amount,
            'f_delivery_amount': f_delivery_amount,
            'is_portal_manager': is_portal_manager,
            'user_id': user_id,
            'company_id': company_id,
            'client_user_ids': client_user_ids,
            'is_project_manager': is_project_manager,
            'js_employees': js_employees,
            'js_server_data': js_server_data,
            'env_user': env_user,
            'dld_plus_6_hour': dld_plus_6_hour,
            'js_clients': js_clients,
            'platform_sources': platform_sources,
            'json_all_profiles': json_all_profiles,
            'employee_id': employee_id,
        })

    """
    Update sale
    """

    @http.route('/portal/sales/update', auth='user')
    def portal_sales_update(self, **kw):

        def get_datetime(datetime_string):
            # Example input from a datetime-local input
            delivery_last_date = datetime_string

            # Parse the input string to a datetime object
            dt_object = datetime.strptime(delivery_last_date, "%Y-%m-%dT%H:%M")

            # Convert the datetime object to UTC if needed
            # Assuming the input datetime is in local time and needs conversion to UTC
            # Replace with your local timezone
            local_tz = pytz.timezone("Asia/Dhaka")
            local_dt = local_tz.localize(dt_object)
            utc_dt = local_dt.astimezone(pytz.utc)

            # Format the datetime object for Odoo's Datetime field
            odoo_formatted_datetime = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
            return odoo_formatted_datetime

        pt = get_partner()
        if not pt:
            return 'Partner not found'

        is_portal_manager = pt.operation_manager

        order_id = kw.get('order_id')
        if not order_id:
            return 'order_id not found'

        order_id = int(order_id)

        order = req.env['sale.order'].sudo().search([('id', '=', order_id)])
        print('order', order)
        if not order:
            return 'Order object not found'

        user_id = req.env.user.id
        print('user_id', user_id)

        order.order_link = kw.get('order_link')
        order.instruction_sheet_link = kw.get('instruction_sheet_link')
        order.special_remarks = kw.get('special_remarks')

        order.assigned_team_id = int(kw.get('assigned_team_id')) if kw.get(
            'assigned_team_id') else None
        order.delivered_team_id = int(kw.get('delivered_team_id')) if kw.get(
            'delivered_team_id') else None
        order.order_status = kw.get('order_status')
        order.teams_delivery_date = kw.get('teams_delivery_date')
        order.order_status = kw.get('order_status')  # later

        platform_source_id = kw.get('platform_source_id')
        order_source_id = kw.get('order_source_id')
        profile_id = kw.get('profile_id')
        client_user_id = kw.get('client_user_id')
        service_type_id = kw.get('service_type_id')
        incoming_date = kw.get('incoming_date')

        amount = kw.get('amount')
        percentage = kw.get('percentage')
        charges_amount = kw.get('charges_amount')
        delivery_amount = kw.get('delivery_amount')

        sales_employee_id = kw.get('sales_employee_id')

        vals = {
            'platform_source_id': int(platform_source_id) if platform_source_id else None,
            'order_source_id': int(order_source_id) if order_source_id else None,
            'profile_id': int(profile_id) if profile_id else None,
            'client_user_id': int(client_user_id) if client_user_id else None,
            'order_number': kw.get('order_number'),
            'service_type_id': int(service_type_id) if service_type_id else None,
            'incoming_date': incoming_date,
            'amount': float(amount) if amount else None,
            'percentage': percentage if percentage else None,
            'charges_amount': float(charges_amount) if charges_amount else None,
            'delivery_amount': float(delivery_amount) if delivery_amount else None,
            'delivery_last_date': get_datetime(kw.get('delivery_last_date')),
            'sales_employee_id': int(sales_employee_id) if sales_employee_id else None,
        }

        print('vals2', vals)

        # client_user_id posted and backend also populated
        if client_user_id and order.client_user_id:
            order.client_user_id.mp_customer_fullname = kw.get('client_name')
            order.client_user_id.email = kw.get('client_email')
            order.client_user_id.phone = kw.get('client_phone')
            """
            client_name
            client_email
            client_phone            
            """

        is_updated = order.write(vals)
        print('is_updated:', is_updated)

        if kw.get('operation_employee_id'):
            order.operation_employee_id = int(kw.get('operation_employee_id'))

        return req.render('bd_portal.update_sale', {
            'order': order,
        })

    # Requisition
    @http.route('/portal/requisition', auth='user', csrf=False)
    def portal_requisition(self, **kw):
        user_id = req.env.user.id
        user_id2 = req.env.user

        if not user_id:
            return 'User ID not found'

        employee_id = req.env['hr.employee'].sudo().search(
            [('user_id2', '=', user_id)], limit=1)
        if not employee_id:
            return 'employee_id not found'

        requisitions = []
        if employee_id:
            requisitions = req.env['cus.purchase.requisition'].sudo().search(
                [('employee_id', '=', employee_id.id)])

        product = req.env['product.product'].sudo().search(
            [('is_purchase_requisition', '=', True)])
        new_req = None
        # req.session['requisition_request'] = True

        if kw.get('form_posted'):
            print('csrf_token', kw.get('csrf_token'))
            print('kw', kw)

            file = kw.get('attach_files')

            req_vals = {
                # 'employee_id': request.env.user.employee_id.id,  # assuming the logged-in user is an employee
                'employee_id': employee_id.id,
                'team_id': kw.get('team_id') if kw.get('team_id') else None,
                'company_id': request.env.user.company_id.id if request.env.user.company_id else None,
                'deadline': kw.get('deadline') if kw.get('deadline') else None,
                'req_from': kw.get('req_from'),
                'alternative_products': kw.get('alternative_products') if kw.get('alternative_products') else None,
                'priority': kw.get('priority') if kw.get('priority') else None,
            }

            print('req_vals', req_vals)

            # Create the purchase requisition record
            new_req = request.env['cus.purchase.requisition'].sudo().create(
                req_vals)

            # Product process
            product_lines = None
            product_lines = kw.get('product_lines')
            _product_lines = None

            if product_lines:
                _product_lines = json.loads(kw.get('product_lines'))

            for product in _product_lines:
                request.env['requisition.order.line'].sudo().create({
                    'requisition_id': new_req.id,
                    'product_id': int(product.get('product_id')),
                    'name': product.get('description'),
                    'quantity': product.get('quantity'),
                    'purpose_of_use': product.get('purpose_of_use'),
                })

            # Shamiul
            # products = json.loads(kw.get('products'))
            # print('products', products)
            # for product in products:
            #     request.env['requisition.order.line'].sudo().create({
            #         'requisition_id': new_req.id,
            #         'product_id': product['product'],
            #         'name': product['description'],
            #         'quantity': product['quantity'],
            #         'purpose_of_use': product['purpose'],
            #
            #     })
            # End  Shamiul

            print('kw', kw)

            if new_req:

                # Attachment process
                files = request.httprequest.files
                attachment_ids = []

                if files:

                    attach_files = files.getlist('attach_files')

                    if attach_files:

                        for attach_file in attach_files:

                            # attachment = req.env['ir.attachment'].sudo().create({
                            #     'name': attach_file.filename,
                            #     'type': 'binary',
                            #     'datas': base64.b64encode(attach_file.read()),
                            #     'store_fname': str(new_req.id),
                            #     'res_model': 'cus.purchase.requisition',
                            #     'res_field': 'attachment_ids',
                            #     'res_id': new_req.id,
                            #     # 'mimetype': 'application/x-pdf'
                            # })

                            attachment = req.env['bd.req.attachment'].sudo().create({
                                'name': attach_file.filename,
                                'file': base64.b64encode(attach_file.read()),
                                'res_model': 'cus.purchase.requisition',
                                'res_id': new_req.id,
                            })

                            if attachment:
                                attachment_ids.append(attachment.id)

                new_req.attachment_ids = attachment_ids
                # End Attachment process

                # alternative_product_file_ids
                _alt_pd_files = request.httprequest.files
                alt_pd_att_ids = []

                if _alt_pd_files:

                    alt_pd_files = files.getlist(
                        'alternative_product_file_ids')

                    if alt_pd_files:

                        for alt_pd_file in alt_pd_files:

                            new_alt_pd_file = req.env['bd.file'].sudo().create({
                                'name': alt_pd_file.filename,
                                'file': base64.b64encode(alt_pd_file.read()),
                                'res_model': 'cus.purchase.requisition',
                                'res_id': new_req.id,
                            })

                            if new_alt_pd_file:
                                alt_pd_att_ids.append(new_alt_pd_file.id)

                new_req.alternative_product_file_ids = alt_pd_att_ids
                # End alternative_product_file_ids

                # req.session['new_req'] = True
                return redirect(f'/portal/requisition/status?new_requisition_id={new_req.id}')

        # Are approve permission?
        is_approve_permission = False

        env_user = req.env.user
        if env_user.department_head or env_user.it_department or env_user.admin_department or env_user.finance_department or env_user.scm_department:
            is_approve_permission = True

        # Project Information
        is_project_manager = False
        if env_user.department_head or env_user.it_department:
            is_project_manager = True

        is_req_req_permission = True
        if user_id2.department_head or user_id2.it_department or user_id2.admin_department or user_id2.finance_department or user_id2.scm_department or user_id2.is_ceo:
            is_req_req_permission = False
            return redirect('/portal/requisition/approval')

        teams = req.env['bd.team'].search([])

        return req.render('bd_portal.requisition', {
            'requisitions': requisitions,
            'employee_id': employee_id,
            'is_approve_permission': is_approve_permission,
            'is_project_manager': is_project_manager,
            'is_req_req_permission': is_req_req_permission,
            'product': product,
            'teams': teams,
        })

    # Requisition status
    @http.route('/portal/requisition/status', auth='user')
    def portal_requisition_status(self, **kw):

        new_req_id = None
        if kw.get('new_requisition_id'):
            new_req_id = req.env['cus.purchase.requisition'].sudo().search(
                [('id', '=', int(kw.get('new_requisition_id')))])

        return req.render('bd_portal.requisition_status', {
            'new_req_id': new_req_id,
        })

    # Requisition approval
    @http.route('/portal/requisition/approval', auth='user')
    def portal_requisition_approval(self, **kw):

        user_id = req.env.user
        user_id_id = req.env.user.id
        is_filter = False

        if not user_id or not user_id_id:
            return 'User ID not found'

        user_id_company_id = user_id.company_id.id if user_id.company_id else None
        if not user_id_company_id:
            return 'User company not found'

        employee_id = req.env['hr.employee'].sudo().search(
            [('user_id2', '=', user_id_id)])
        if not employee_id:
            return 'employee_id not found'

        """ --------------------------------------
        Filter
        -------------------------------------- """
        # Filter domain
        filter_domain = []

        # Append company domain
        # if user_id.department_head or user_id.it_department: Previous
        if user_id.department_head or user_id.it_department:

            # department_head if filtered by company but not it_department
            if user_id.department_head:
                filter_domain.append(
                    ('company_id', '=', user_id.company_id.id))

            # Append domain for it
            if user_id.it_department:
                filter_domain.append(('req_from', '=', 'it'))

        # Filters
        filter_requisition_id = kw.get('filter_requisition_id')
        filter_department = kw.get('filter_department')
        filter_status = kw.get('filter_status')
        filter_company_id = kw.get('filter_company_id')
        filter_department_value = False

        # Filter by id
        if filter_requisition_id:
            filter_domain.append(('name', '=', filter_requisition_id))
            is_filter = True

        # Filter by other things
        elif filter_department:

            print('filter_department:', filter_department)
            filter_department_value = True
            is_filter = True

            full_path = req.httprequest.full_path
            req.session['full_path'] = full_path

            # department_head
            if filter_department == 'department_head':

                # Filter by status
                if filter_status == 'accepted':
                    filter_domain.append(
                        ('department_head_state', '=', 'accepted'))

                elif filter_status == 'cancelled':
                    filter_domain.append(
                        ('department_head_state', '=', 'canceled'))

                elif filter_status == 'to_approve':
                    filter_domain.append(
                        ('department_head_state', '!=', 'canceled'))
                    filter_domain.append('|')
                    filter_domain.append(('app_state', '=', ''))
                    filter_domain.append(('app_state', '=', 'draft'))

            # it_department
            elif filter_department == 'it_department':

                # # Filter by status
                # if filter_status == 'accepted':
                #
                #     filter_domain.append('&')
                #     filter_domain.append(('it_department_state', '=', 'accepted'))
                #     print('filter_status', filter_status)
                #
                # elif filter_status == 'cancelled':
                #
                #     filter_domain.append('&')
                #     filter_domain.append(('it_department_state', '=', 'canceled'))
                #     print('filter_status', filter_status)
                #
                # filter_domain.append('|')
                # filter_domain.append(('app_state', '=', 'approve_dh'))
                # filter_domain.append(('app_state', '=', 'approve_it'))

                if filter_status == 'accepted':
                    filter_domain.append(
                        ('it_department_state', '=', 'accepted'))

                elif filter_status == 'cancelled':
                    filter_domain.append(
                        ('it_department_state', '=', 'canceled'))

                elif filter_status == 'to_approve':

                    filter_domain.append(
                        ('department_head_state', '=', 'accepted'))
                    filter_domain.append(
                        ('it_department_state', '!=', 'canceled'))
                    filter_domain.append(('app_state', '=', 'approve_dh'))

            # admin_department
            elif filter_department == 'admin_department':

                # # Filter by status
                # if filter_status == 'accepted':
                #
                #     filter_domain.append('&')
                #     filter_domain.append(('admin_department_state', '=', 'accepted'))
                #     print('filter_status', filter_status)
                #
                #     filter_domain.append('|')
                #     filter_domain.append(('app_state', '=', 'approve_it'))
                #     filter_domain.append(('app_state', '=', 'approve_admin'))
                #
                # elif filter_status == 'cancelled':
                #
                #     filter_domain.append('&')
                #     filter_domain.append(('admin_department_state', '=', 'canceled'))
                #     print('filter_status cancelled', filter_status)
                #
                #     filter_domain.append('|')
                #     filter_domain.append(('app_state', '=', 'approve_dh'))
                #     filter_domain.append(('app_state', '=', 'approve_it'))
                #
                # else:
                #     filter_domain.append('|')
                #     filter_domain.append('|')
                #     filter_domain.append(('app_state', '=', 'approve_it'))
                #     filter_domain.append(('app_state', '=', 'approve_admin'))
                #     filter_domain.append(('app_state', '=', 'approve_dh'))

                # scm_department - Done

                if filter_status == 'accepted':
                    filter_domain.append(
                        ('admin_department_state', '=', 'accepted'))

                elif filter_status == 'cancelled':
                    filter_domain.append(
                        ('admin_department_state', '=', 'canceled'))

                elif filter_status == 'to_approve':
                    filter_domain.append(
                        ('admin_department_state', '!=', 'canceled'))
                    filter_domain.append('|')
                    filter_domain.append(('app_state', '=', 'approve_dh'))
                    filter_domain.append(('app_state', '=', 'approve_it'))

            elif filter_department == 'scm_department':

                if filter_status == 'accepted':
                    filter_domain.append(
                        ('scm_department_state', '=', 'accepted'))

                elif filter_status == 'cancelled':
                    filter_domain.append(
                        ('scm_department_state', '=', 'canceled'))

                elif filter_status == 'to_approve':
                    filter_domain.append(
                        ('admin_department_state', '=', 'accepted'))
                    filter_domain.append(
                        ('scm_department_state', '!=', 'canceled'))
                    filter_domain.append(('app_state', '=', 'approve_admin'))

            # finance_department - Done
            elif filter_department == 'finance_department':

                if filter_status == 'accepted':
                    filter_domain.append(
                        ('finance_department_state', '=', 'accepted'))

                elif filter_status == 'cancelled':
                    filter_domain.append(
                        ('finance_department_state', '=', 'canceled'))

                elif filter_status == 'to_approve':
                    filter_domain.append(
                        ('scm_department_state', '=', 'accepted'))
                    filter_domain.append(
                        ('finance_department_state', '!=', 'canceled'))
                    filter_domain.append(('app_state', '=', 'approve_scm'))

        elif filter_company_id:

            # Filter by company
            if filter_company_id:
                # filter_domain.append('&')
                filter_domain.append(
                    ('company_id', '=', int(filter_company_id)))
                print('filter_company_id:', filter_company_id)

        print('filter_domain:', filter_domain)
        """ --------------------------------------
        End Filter
        -------------------------------------- """

        my_requisition_objects = req.env['cus.purchase.requisition'].sudo().search(
            filter_domain)
        my_requisitions = []

        for requisition in my_requisition_objects:
            values = {
                'requisition': requisition,
                'can_i_approve': False,
            }

            # Can I Approve (department_head)
            if user_id.department_head:

                if requisition.app_state == '' or requisition.app_state is None or requisition.app_state == 'draft':
                    values['can_i_approve'] = True

            # Can I Approve (it_department)
            elif requisition.req_from == 'it' and user_id.it_department:

                if requisition.app_state == 'approve_dh':
                    values['can_i_approve'] = True

            # Can I Approve - admin_department
            elif user_id.admin_department:

                if requisition.req_from == 'it' and requisition.app_state == 'approve_it':
                    values['can_i_approve'] = True

                elif requisition.req_from == 'admin' and requisition.app_state == 'approve_dh':
                    values['can_i_approve'] = True
                else:
                    pass

            # Can I Approve - scm_department
            elif user_id.scm_department:

                if requisition.app_state == 'approve_admin':  # Changed
                    values['can_i_approve'] = True

            # Can I Approve - finance_department
            elif user_id.finance_department:

                if requisition.app_state == 'approve_scm':  # Changed
                    values['can_i_approve'] = True

            # Ceo
            elif user_id.is_ceo:

                if requisition.app_state == 'approve_finance':
                    values['can_i_approve'] = True

            else:
                pass
            """
            draft

            approve_dh
            approve_it
            approve_admin
            approve_finance
            approve_scm

            done
            cancel
            """

            my_requisitions.append(values)

        approval_info = req.session.get('approval_info')
        req.session.pop('approval_info', None)

        # Who able to access requisition
        is_req_req_permission = True
        if user_id.department_head or user_id.it_department or user_id.admin_department or user_id.finance_department or user_id.scm_department or user_id.is_ceo:
            is_req_req_permission = False
        else:
            return redirect('/portal/requisition')

        _full_path = req.session.get('full_path')
        is_redirected = req.session.get('is_redirected')
        if _full_path and not is_redirected:
            print('full_path f')
            req.session.pop('full_path', None)
            req.session['is_redirected'] = True
            return redirect(_full_path)

        return req.render('bd_portal.requisition_approval', {
            'employee_id': employee_id,
            'user_id': user_id,
            'approval_info': approval_info,
            'my_requisitions': my_requisitions,
            'is_req_req_permission': is_req_req_permission,
            'is_filter': is_filter,
            'kw': kw,
            'filter_department_value': filter_department_value,
            'filter_department': filter_department,
        })

    # Requisition approval action
    @http.route('/portal/requisition/approval/action', auth='user')
    def portal_requisition_approval_action(self, **kw):

        user_id = req.env.user
        print('user_id', user_id)
        user_id_id = req.env.user.id

        if not user_id or not user_id_id:
            return 'User ID not found'

        employee_id = req.env['hr.employee'].sudo().search(
            [('user_id2', '=', user_id_id)])
        print('employee_id', employee_id)

        if not employee_id:
            return 'employee_id not found'

        """
        Action codes
        """
        action = kw.get('action')
        requisition_id = kw.get('requisition_id')

        if not action or not requisition_id:
            return 'action param/value or requisition_id not found'

        print('Action for approve')
        requisition = req.env['cus.purchase.requisition'].sudo().search(
            [('id', '=', int(requisition_id))])
        print('requisition', requisition)

        if not requisition:
            return 'requisition object not found'

        if action == 'APPROVE':

            # Set accepted state by user (it and admin both)
            if user_id.department_head:
                requisition.app_state = 'approve_dh'
                requisition.department_head_state = 'accepted'
                requisition.approval_date_department_head = date.today()

            elif user_id.it_department:
                requisition.app_state = 'approve_it'
                requisition.it_department_state = 'accepted'
                requisition.approval_date_it_department = date.today()

            elif user_id.admin_department:
                requisition.app_state = 'approve_admin'
                requisition.admin_department_state = 'accepted'
                requisition.approval_date_admin_department = date.today()

            elif user_id.scm_department:
                requisition.app_state = 'approve_scm'
                requisition.scm_department_state = 'accepted'
                requisition.approval_date_scm_department = date.today()

                if kw.get('budget'):
                    requisition.budget = float(kw.get('budget'))

            elif user_id.finance_department:
                requisition.app_state = 'approve_finance'
                requisition.finance_department_state = 'accepted'
                requisition.approval_date_finance_department = date.today()

                if kw.get('budget_pass_date'):
                    requisition.budget_pass_date = kw.get('budget_pass_date')

            elif user_id.is_ceo:
                requisition.app_state = 'approve_ceo'
                requisition.ceo_state = 'accepted'
                requisition.approval_date_ceo = date.today()

            else:
                pass

            req.session['approval_info'] = f'<div> <strong>{requisition.name}\'s</strong> state updated</div>'

        elif action == 'REJECT':
            print('Action for reject block')
            requisition.app_state = 'cancel'

            # Set Cancel state by user (it and admin both)
            if user_id.department_head:
                requisition.department_head_state = 'canceled'
                requisition.approval_date_department_head = date.today()

            elif user_id.it_department:
                requisition.it_department_state = 'canceled'
                requisition.approval_date_it_department = date.today()

            elif user_id.admin_department:
                requisition.admin_department_state = 'canceled'
                requisition.approval_date_admin_department = date.today()

            elif user_id.scm_department:
                requisition.scm_department_state = 'canceled'
                requisition.approval_date_scm_department = date.today()

            elif user_id.finance_department:
                requisition.finance_department_state = 'canceled'
                requisition.approval_date_finance_department = date.today()

                values = {
                    'department': 'finance',
                    'name': 'Rejected by finance',
                    'req_id': requisition.id,
                }
                fin_not = req.env['bd.notification'].sudo().create(values)

            elif user_id.is_ceo:
                requisition.ceo_state = 'canceled'
                requisition.approval_date_ceo = date.today()

            else:
                pass

            req.session[
                'approval_info'] = f'<div> <strong>{requisition.name}\'s</strong> state changed to Canceled</div>'

        return redirect('/portal/requisition/approval')

    @http.route('/portal/notifications', auth='user')
    def portal_notifications(self, **kw):

        # Finance Notifications
        user = req.env.user
        fin_not = None

        if user.scm_department:
            fin_not = req.env['bd.notification'].sudo().search(
                [('department', '=', 'finance')], limit=50)

            if fin_not:
                for fin_nt in fin_not:
                    fin_nt.mark_as_read = True

        return req.render('bd_portal.notifications', {
            'fin_not': fin_not,
        })

    @http.route('/f_sales_employee_id', type='http', auth='none', cors='*', csrf=False)
    def f_sales_employee_id(self, **kw):

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

        # Get employee object from search
        query = kw.get('query')
        employees = req.env['hr.employee'].sudo().search([
            '|', '|',
            ('name', 'ilike', query),
            ('work_phone', 'ilike', query),
            ('work_email', 'ilike', query),
        ], limit=5)

        print('employees', employees)

        if employees:

            emp_recs = []

            for emp in employees:
                vals = {
                    'id': emp.id,
                    'name': emp.name,
                    'other': 'other',
                    'url': f'/portal/sales?page=1&f_sales_employee_id={emp.id}',
                }

                emp_recs.append(vals)

            success_response['data'] = emp_recs
            return json.dumps(success_response)

        else:
            return json.dumps(error_response)

    @http.route('/f_platform_source', type='http', auth='none', cors='*', csrf=False)
    def f_platform_source(self, **kw):

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

        # Get employee object from search
        query = kw.get('query')
        records = req.env['bd.platform_source'].sudo().search([
            ('name', 'ilike', query),
        ], limit=5)

        print('records', records)

        if records:

            recs = []

            for rec in records:
                vals = {
                    'id': rec.id,
                    'name': rec.name,
                    'url': f'/portal/sales?page=1&f_platform_source_id={rec.id}',
                }

                recs.append(vals)

            success_response['data'] = recs
            return json.dumps(success_response)

        else:
            return json.dumps(error_response)

    @http.route('/f_order_source', type='http', auth='none', cors='*', csrf=False)
    def f_order_source(self, **kw):

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

        # Get employee object from search
        query = kw.get('query')
        records = req.env['bd.order_source'].sudo().search([
            ('name', 'ilike', query),
        ], limit=5)

        print('records', records)

        if records:

            recs = []

            for rec in records:
                vals = {
                    'id': rec.id,
                    'name': rec.name,
                    'url': f'/portal/sales?page=1&f_order_source_id={rec.id}',
                }

                recs.append(vals)

            success_response['data'] = recs
            return json.dumps(success_response)

        else:
            return json.dumps(error_response)

    @http.route('/f_profile_id', type='http', auth='none', cors='*', csrf=False)
    def f_profile_id(self, **kw):

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

        # Get employee object from search
        query = kw.get('query')
        records = req.env['bd.profile'].sudo().search([
            ('name', 'ilike', query),
        ], limit=5)

        print('records', records)

        if records:

            recs = []

            for rec in records:
                vals = {
                    'id': rec.id,
                    'name': f'{rec.name}{" - " + rec.platform_source_id.name if rec.platform_source_id else None}',
                    'url': f'/portal/sales?page=1&f_profile_id={rec.id}',
                }

                recs.append(vals)

            success_response['data'] = recs
            return json.dumps(success_response)

        else:
            return json.dumps(error_response)

    @http.route('/f_client_user_id', type='http', auth='none', cors='*', csrf=False)
    def f_client_user_id(self, **kw):

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

        # Get employee object from search
        query = kw.get('query')
        records = req.env['res.partner'].sudo().search([
            ('mp_customer_fullname', 'ilike', query),
            ('is_mp_customer', '=', True),
        ], limit=5)

        print('records', records)

        if records:

            recs = []

            for rec in records:
                vals = {
                    'id': rec.id,
                    'name': rec.mp_customer_fullname,
                    'url': f'/portal/sales?page=1&f_client_user_id={rec.id}',
                }

                recs.append(vals)

            success_response['data'] = recs
            return json.dumps(success_response)

        else:
            return json.dumps(error_response)

    @http.route('/f_order_id', type='http', auth='none', cors='*', csrf=False)
    def f_order_id(self, **kw):

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

        # Get employee object from search
        query = kw.get('query')
        records = req.env['sale.order'].sudo().search([
            ('order_number', 'ilike', query),
        ], limit=5)

        print('records', records)

        if records:

            recs = []

            for rec in records:
                vals = {
                    'id': rec.id,
                    'name': rec.order_number,
                    'url': f'/portal/sales?page=1&f_order_id={rec.order_number}',
                }

                recs.append(vals)

            success_response['data'] = recs
            return json.dumps(success_response)

        else:
            return json.dumps(error_response)

    @http.route('/ajax_requisition_get_products', type='http', auth='none', cors='*', csrf=False)
    def ajax_requisition_get_products(self, **kw):

        print('ajax_requisition_get_products called')

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

        # Get employee object from search
        query = kw.get('query')
        products = req.env['product.product'].sudo().search([
            ('is_purchase_requisition', '=', True),
            ('name', 'ilike', query)
        ], limit=5)

        print('products', products)

        if not products:
            return json.dumps(error_response)

        pd_recs = []

        for product in products:
            vals = {
                'id': product.id,
                'name': product.name,
                'other': 'other',
                'url': f'/portal/sales?page=1&f_sales_employee_id={product.id}',
            }

            pd_recs.append(vals)

        success_response['data'] = pd_recs
        return json.dumps(success_response)

    @http.route('/t666', type='http', auth='none', cors='*', csrf=False)
    def t666(self, **kw):

        # sale = req.env['sale.order'].sudo().search([('id', '=', 4301)])
        # order_line = sale.order_line
        # print('order_line', order_line)
        #
        # for line in order_line:
        #     print(line.price_unit)

        # full_path = req.httprequest.full_path
        # req.session['full_path'] = full_path

        req.session['is_redirected'] = False

        return 't666'

    @http.route('/portal/requisition/approval/save_session', type='http', auth='none', csrf=False)
    def requisition_save_session(self, **kw):

        # full_path = req.httprequest.full_path
        # req.session['full_path'] = full_path
        req.session['is_redirected'] = False

        return redirect('/portal/dashboard')
