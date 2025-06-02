# -*- coding: utf-8 -*-
import calendar
import json
import logging
from collections import defaultdict
from odoo import http
from odoo.http import request, request as req
from datetime import datetime, time, date, timedelta
from werkzeug.utils import redirect
import base64
import math
from odoo.addons.portal.controllers.portal import pager as portal_pager


_logger = logging.getLogger(__name__)


class PurchaseRequisition(http.Controller):

    # Requisition
    @http.route('/portal/requisition', auth='user', csrf=False, website=True)
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
                line_vals = {
                    'requisition_id': new_req.id,
                    'product_id': int(product.get('product_id')),
                    'name': product.get('description'),
                    'quantity': product.get('quantity'),
                    'purpose_of_use': product.get('purpose_of_use'),
                }

                product_id = product.get('id')
                file_field_name = f'product_line_file_{product_id}'

                if file_field_name in request.httprequest.files:
                    file_data = request.httprequest.files[file_field_name]
                    if file_data:
                        # line_vals['file_name'] = file_data.filename
                        line_vals['file_attachment'] = base64.b64encode(
                            file_data.read())

                request.env['requisition.order.line'].sudo().create(line_vals)

            if new_req:
                # Attachment process
                files = request.httprequest.files
                attachment_ids = []

                if files and 'attach_files' in files:
                    attach_files = files.getlist('attach_files')

                    if attach_files:
                        for attach_file in attach_files:
                            if attach_file.filename:  # Only process if there's a filename
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

                if _alt_pd_files and 'alternative_product_file_ids' in _alt_pd_files:
                    alt_pd_files = files.getlist(
                        'alternative_product_file_ids')

                    if alt_pd_files:
                        for alt_pd_file in alt_pd_files:
                            if alt_pd_file.filename:  # Only process if there's a filename
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

        return req.render('sales_portal_bdcalling.requisition', {
            'requisitions': requisitions,
            'employee_id': employee_id,
            'is_approve_permission': is_approve_permission,
            'is_project_manager': is_project_manager,
            'is_req_req_permission': is_req_req_permission,
            'product': product,
            'teams': teams,
        })

    # Requisition dashboard
    @http.route(['/portal/requisition/dashboard','/portal/requisition/dashboard/page/<int:page>'], type='http', auth='user', website=True)
    def portal_requisition_dashboard(self, **kw):
        user_id = req.env.user.id
        user_id2 = req.env.user

        if not user_id:
            return 'User ID not found'

        employee_id = req.env['hr.employee'].sudo().search(
            [('user_id2', '=', user_id)], limit=1)
        if not employee_id:
            return 'employee_id not found'
        search_value = kw.get('search_value', '')
        page = int(kw.get('page', 1)) or 1
        per_page = 10
        offset = (page - 1) * per_page
        domain = []


        if employee_id:
            domain = [('employee_id', '=', employee_id.id)]
        
        orders = req.env['cus.purchase.requisition'].sudo().search(domain)
        if search_value:
            domain = ['|',
                ('name', '=', search_value),
                ('employee_id.name', '=', search_value),
            ]
            orders = request.env['cus.purchase.requisition'].sudo().search(domain)
            if not orders:
                domain = ['|',
                    ('name', 'ilike', search_value),
                    ('employee_id.name', 'ilike', search_value),
                ]
                orders = request.env['cus.purchase.requisition'].sudo().search(domain)
                
        filtered_orders = orders.sudo().search(domain)
        total_count = len(filtered_orders)
        total_pages = math.ceil(total_count / per_page)
        final_orders = filtered_orders[offset:offset + per_page]
        pager = portal_pager(
            url="/portal/requisition/dashboard",
            url_args={'search': search_value},
            total=total_count,
            page=page,
            step=per_page,
            scope=5,
        )        

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

        return req.render('sales_portal_bdcalling.requisition_dashboard', {
            'employee_id': employee_id,
            # 'user_id': user_id,
            'search_value': search_value,
            'page': page,
            'pager': pager,
            'total_pages': total_pages,
            'requisitions': final_orders,
            'is_approve_permission': is_approve_permission,
            'is_project_manager': is_project_manager,
            'is_req_req_permission': is_req_req_permission,
        })

    # Requisition status
    @http.route('/portal/requisition/status', auth='user', website=True)
    def portal_requisition_status(self, **kw):

        new_req_id = None
        if kw.get('new_requisition_id'):
            new_req_id = req.env['cus.purchase.requisition'].sudo().search(
                [('id', '=', int(kw.get('new_requisition_id')))])

        return req.render('sales_portal_bdcalling.requisition_status', {
            'new_req_id': new_req_id,
        })

    # Requisition approval
    @http.route('/portal/requisition/approval', auth='user', website=True)
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

        return req.render('sales_portal_bdcalling.requisition_approval', {
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
    @http.route('/portal/requisition/approval/action', auth='user', website=True)
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
                'url': f'/sale/dashboard?page=1&f_sales_employee_id={product.id}',
            }

            pd_recs.append(vals)

        success_response['data'] = pd_recs
        return json.dumps(success_response)

    @http.route('/ajax_upload_product_file', type='http', auth='user', csrf=False)
    def ajax_upload_product_file(self, **kw):
        try:
            files = request.httprequest.files
            if not files or 'file' not in files:
                return json.dumps({
                    'status': 'error',
                    'message': 'No file uploaded'
                })

            uploaded_file = files.get('file')
            file_content = base64.b64encode(uploaded_file.read())

            return json.dumps({
                'status': 'success',
                'data': {
                    'file_content': file_content.decode('utf-8'),
                    'file_name': uploaded_file.filename
                }
            })
        except Exception as e:
            _logger.error(f"Error in ajax_upload_product_file: {str(e)}")
            return json.dumps({
                'status': 'error',
                'message': str(e)
            })

    @http.route('/portal/requisition/approval/save_session', type='http', auth='none', csrf=False)
    def requisition_save_session(self, **kw):

        # full_path = req.httprequest.full_path
        # req.session['full_path'] = full_path
        req.session['is_redirected'] = False

        return redirect('/bdcalling/dashboard')

    # Notifications

    @http.route('/portal/notifications', auth='user', website=True)
    def portal_notifications(self, **kw):
        user = request.env.user
        fin_not = []

        if user.scm_department:
            fin_not = request.env['bd.notification'].sudo().search([
                ('department', '=', 'finance')
            ], limit=50)
            print("fin_not:", fin_not)

            if fin_not:
                fin_not.sudo().write({'mark_as_read': True})
                print("ded")

        return request.render('sales_portal_bdcalling.notifications', {
            'fin_not': fin_not,
            # Ensure 'languages' is always available
            'languages': request.env['res.lang'].search([]),
        })

    @http.route('/bdcalling/dashboard', auth='user', website=True)
    def portal_dashboard(self, **kw):
        user_id = request.env.user
        current_date = date.today()

        # First and Last Day of the Current Month
        first_day_of_month = datetime(current_date.year, current_date.month, 1)
        last_day = calendar.monthrange(
            current_date.year, current_date.month)[1]

        if current_date.month == 12:
            last_day_of_month = datetime(current_date.year, 12, 31)
        else:
            last_day_of_month = datetime(
                current_date.year, current_date.month + 1, 1) - timedelta(days=1)

        # Set time components
        first_day_of_month = first_day_of_month.replace(
            hour=0, minute=0, second=0)
        last_day_of_month = last_day_of_month.replace(
            hour=23, minute=59, second=59)

        # Sales Data
        total_order = request.env['sale.order'].sudo().search_count([
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('company_id', '=', user_id.company_id.id),
        ])

        total_wip = request.env['sale.order'].sudo().search_count([
            ('order_status', '=', 'wip'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
        ])

        total_completed = request.env['sale.order'].sudo().search_count([
            ('order_status', '=', 'complete'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
        ])

        # Best Sales Performer
        sales = request.env['sale.order'].sudo().search([
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('order_status', '!=', 'cancelled'),
        ])

        sales_totals = defaultdict(float)
        for sale in sales:
            sales_totals[sale.sales_employee_id.id] += sale.amount_total

        best_employee_id = max(
            sales_totals, key=sales_totals.get, default=None)
        best_sale_performer = request.env['hr.employee'].sudo().search(
            [('id', '=', best_employee_id)]) if best_employee_id else None

        # Best Delivery Performer
        sales_delivered = request.env['sale.order'].sudo().search([
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            '|',
            ('order_status', '=', 'delivered'),
            ('order_status', '=', 'complete'),
        ])

        sales_totals_d = defaultdict(float)
        for sale_d in sales_delivered:
            sales_totals_d[sale_d.delivered_team_id.id] += sale_d.amount_total

        best_team_id = max(
            sales_totals_d, key=sales_totals_d.get, default=None)
        best_delivery_team_id = request.env['assign.team'].sudo().search(
            [('id', '=', best_team_id)]) if best_team_id else None

        # Purchase Requisition
        total_pr_count = request.env['cus.purchase.requisition'].sudo().search_count([
        ])
        total_ceo_acc_count = request.env['cus.purchase.requisition'].sudo().search_count([
            ('ceo_state', '=', 'accepted')
        ])

        # Check Purchase Access
        purchase_access = any([
            user_id.department_head,
            user_id.it_department,
            user_id.admin_department,
            user_id.scm_department,
            user_id.finance_department,
            user_id.is_ceo
        ])

        return request.render('sales_portal_bdcalling.dashboard_temp', {
            'total_order': total_order,
            'total_wip': total_wip,
            'total_completed': total_completed,
            'best_sale_performer': best_sale_performer,
            'best_delivery_team_id': best_delivery_team_id,
            'total_pr_count': total_pr_count,
            'total_ceo_acc_count': total_ceo_acc_count,
            'purchase_access': purchase_access,
        })
