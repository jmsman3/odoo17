    
# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.exceptions import ValidationError
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
from odoo.addons.portal.controllers.portal import pager as portal_pager

import logging
_logger = logging.getLogger(__name__)

def get_partner():
    user_id = req.env.user.id
    res_user = req.env['res.users'].sudo().search([('id', '=', user_id)], limit=1)

    if res_user:
        return res_user.partner_id
    else:
        return None
    
class PortalWebsite(http.Controller): 
       
    @http.route(['/sale/quotation'], type='http', auth="user", website=True)
    def quotation_form(self, **kw):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        if not employee:
            return request.redirect('/my')
        products = request.env['product.template'].sudo().search([
            ('portal_available', '=', True),
            ('company_id', '=', request.env.company.id),
        ])
        company_id = req.env.company
        print('company_id:', company_id)
        departments = request.env['hr.department'].sudo().search([])
        profiles = request.env['bd.profile'].sudo().search([('company_id', '=', company_id.id)])
        team_id = request.env['assign.team'].sudo().search([('company_id', '=', user.company_id.id)])
        partners = request.env['res.partner'].sudo().search([('company_id', '=', user.company_id.id)])
        # teams = request.env['assign.team'].sudo().search([('company_id', '=', user.company_id.id)])
        _logger.info('partners_____________________________________________________: %s', partners)
        _logger.info('teams_____________________________________________________: %s', team_id)
        employees = request.env['hr.employee'].sudo().search([])
        mediums = request.env['bd.platform_source'].sudo().search([])
        sources = request.env['bd.order_source'].sudo().search([])
        tags = request.env['crm.tag'].sudo().search([])
        today = fields.Date.today().strftime('%Y-%m-%d')
        values = {
            'products': products,
            'departments': departments,
            'profiles': profiles,
            'mediums': mediums,
            'sources': sources,
            'partners': partners,
            'team_id': team_id,
            # 'teams': teams,
            'tags': tags,
            'employees': employees,
            'employee': employee,
            'today': today,
        }
        return request.render('sales_portal_bdcalling.portal_quotation_form', values)
    
    @http.route(['/sale/create_quotation'], type='json', auth="user", website=True)
    def create_quotation(self, **kw):
        try:
            data = kw
            user = request.env.user
            _logger.info("User: %s", user)
            employee = request.env['hr.employee'].sudo().search([
                ('user_id', '=', user.id)
            ], limit=1)
            _logger.info("Employee: %s", employee)
            if not employee:
                return {'success': False, 'error': 'Invalid user'}
            _logger.info("Received data: %s", data)
            employee_id = kw.get('employee_id')
            _logger.info("Employee ID: %s", employee_id)
            def get_datetime(datetime_string):
                delivery_last_date = datetime_string
                dt_object = datetime.strptime(delivery_last_date, "%Y-%m-%dT%H:%M")
                local_tz = pytz.timezone("Asia/Dhaka") 
                local_dt = local_tz.localize(dt_object)
                utc_dt = local_dt.astimezone(pytz.utc)
                odoo_formatted_datetime = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                return odoo_formatted_datetime
            crm_tag = kw.get('crm_tag_ids')
            tag_id = int(crm_tag) if crm_tag and crm_tag.isdigit() else None

            _logger.info("CRM Tag: %s", crm_tag)
            end_date = get_datetime(kw.get('delivery_last_date'))
            deadline = str(kw.get('deadline'))
            service_type_id = int(kw.get('service_type_id')) if kw.get('service_type_id') else False
            order_number = kw.get('order_number')
            if order_number:
                existing = request.env['sale.order'].sudo().search([('order_number', '=', order_number)], limit=1)
                if existing:
                    return {'success': False, 'message': 'Order number already exists. Please use a unique one.'}

            order_vals = {
                'employee_id': employee.id,
                'partner_id': kw.get('partner_id'),
                'sales_employee_id': kw.get('sales_employee_id'),
                'platform_source_id': kw.get('platform_source_id') if kw.get('platform_source_id') else False,
                'order_source_id': kw.get('order_source_id') if kw.get('order_source_id') else False,
                'profile_id': kw.get('profile_id') if kw.get('profile_id') else False,
                'order_number': order_number,
                'order_link': kw.get('order_link') if kw.get('order_link') else False,
                'instruction_sheet_link': kw.get('instruction_sheet_link') if kw.get('instruction_sheet_link') else False,
                'service_type_id': service_type_id,
                'incoming_date': kw.get('incoming_date'),
                'delivery_last_date': end_date,
                'amount': kw.get('amount'),
                'percentage': kw.get('percentage'),
                'charges_amount': kw.get('charges_amount'),
                'delivery_amount': kw.get('delivery_amount'),
                'special_remarks': kw.get('special_remarks') if kw.get('special_remarks') else False,
                'order_status': kw.get('order_status') if kw.get('order_status') else 'draft',
                'crm_tag_ids': [(6, 0, [tag_id])] if tag_id else False,
                'assign_team_id': kw.get('team_id') if kw.get('team_id') else False, 
                'deadline': deadline,
                
            }
            if service_type_id:
                _logger.info("Product ID: %s", service_type_id)
                service_tmpl_id = request.env['product.template'].sudo().search(
                [('id', '=', service_type_id)])
                _logger.info("Service Template ID: %s", service_tmpl_id)
                if service_tmpl_id:
                    service_product_id = request.env['product.product'].sudo().search(
                        [('product_tmpl_id', '=', service_tmpl_id.id)])
                    _logger.info("Service Product ID: %s", service_product_id)
                    if service_product_id:
                        order_vals['order_line'] = [Command.create({
                            'product_id': service_product_id.id,
                            'product_uom_qty': 1,
                            'price_unit': float(kw.get('delivery_amount')),
                            'tax_id': False,
                        })]
            _logger.info("Order values: %s", order_vals)
            
            order = request.env['sale.order'].sudo().create(order_vals)
            order.action_confirm()

            _logger.info("Created Order---------------------------------------------------1: %s", order)
            if order:
                return {
                    'success': True,
                    'message': 'Quotation created successfully',
                    'order_id': order.id,
                }
            else:
                return {
                    'success': False,
                    'message': 'Please fill the form correctly.',
                }

        except Exception as e:
            _logger.error("Error creating quotation: %s",
                          str(e), exc_info=True)
            return {'success': False, 'error': str(e)}
    
    
    @http.route('/sale/check_order_number', type='json', auth='user')
    def check_order_number(self, order_number):
        existing_order = request.env['sale.order'].sudo().search([('order_number', '=', order_number)], limit=1)
        if existing_order:
            return {'success': False, 'message': 'Order Number already exists'}
        return {'success': True}
    
    
    @http.route(['/partner/search'], type='json', auth="user", website=True)
    def search_items(self, **kw):
        _logger.info("Searching records for model 1________________________:" )

        try:
            model = kw.get('model')
            term = kw.get('term')
            if not model or not term:
                return {'error': 'Missing required parameters'}

            if model == 'res.partner':
                domain = [('name', 'ilike', term),('company_id', '=', request.env.user.company_id.id)]
                fields = ['id', 'name', 'email', 'phone', 'street','city','zip','country_id']
            else:
                return {'error': 'Invalid model'}

            records = request.env[model].sudo().search_read(
                domain=domain,
                fields=fields,
                limit=10
            )
            _logger.info(f"Records found for model {model}________________________: {records}")
            return records
        except Exception as e:
            return {'error': str(e)}
        
        
        
    @http.route(['/rfq/get_partner'], type='json', auth="user", website=True)
    def get_partner_data(self, **kw):
        try:
            partner_id = int(kw.get('partner_id'))
            if not partner_id:
                return {'error': 'No partner ID provided'}
                
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if not partner.exists():
                return {'error': 'Partner not found'}
                
            return {
                'id': partner.id,
                'name': partner.name,
                'email': partner.email or '',
                'phone': partner.phone or '',
                'street': partner.street or '',
                'city': partner.city or '',
                'zip': partner.zip or '',
                'country_id': partner.country_id.name or '',

            }
        except Exception as e:
            return {'error': str(e)}

    @http.route(['/sale/dashboard','/sale/dashboard/page/<int:page>'], type='http', auth="user", website=True)
    def dashboard(self, status=None, assign_team_id=None, year=None, month=None, **kw):

        # Check if the logged-in user is a sales head
        user = request.env.user
        employee_id = request.env['hr.employee'].sudo().search([
                ('user_id', '=', user.id)
            ], limit=1)
        is_sales_head = user.has_group('sales_team.group_sale_manager')
        search_value = kw.get('search_value', '')
        page = int(kw.get('page', 1)) or 1
        per_page = 20
        offset = (page - 1) * per_page
        domain = []
        if user.operation_leader == True:
            domain.append(('assign_team_id.team_leader', '=', user.id))
        if user.sales_man == True:
            domain.append(('employee_id.user_id', '=', user.id))
        if user.sale_leader == True:
            domain.append(('company_id', '=', user.company_id.id))
            
        today = fields.Date.today()
        if year and month:
            start_date = f"{year}-{month}-01"
            end_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=31)
            end_date = end_date.replace(day=1) - timedelta(days=1)
            _logger.info('Start Date____________in if: %s', start_date)
        else:
            start_date = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
            _logger.info('Start Date____________in else: %s', start_date)
            _logger.info('End Date: %s', end_date)
        start_date_str = start_date if isinstance(start_date, str) else start_date.strftime("%Y-%m-%d")
        end_date_str = end_date if isinstance(end_date, str) else end_date.strftime("%Y-%m-%d")
        _logger.info('Start Date: %s', start_date_str)
        _logger.info('End Date: %s', end_date_str)
        # Add date filter to domain
        if year and month:
            domain.append(('incoming_date', '>=', start_date_str))
            domain.append(('incoming_date', '<=', end_date_str))
        if status:
            domain.append(('order_status', '=', status))
            _logger.info('Filtered Orders: %s', domain)
        if assign_team_id:
            domain.append(('assign_team_id', '=', int(assign_team_id)))
            _logger.info('Filtered Orders: %s', domain)

        orders = request.env['sale.order'].sudo().search(domain)
        total_sales = sum(orders.mapped('amount_total'))

        # Search for KPI records for this employee and date range
        kpi_domain = [
            ('employee_id', '=', employee_id.id),
            ('period_start', '<=', start_date_str),
            ('period_end', '>=', end_date_str)
        ]
        _logger.info('KPI Domain: %s', kpi_domain)
        kpi_record = request.env['employee.kpi'].sudo().search(kpi_domain, limit=1)
        _logger.info('KPI Record: %s', kpi_record)
        minimum_target = employee_id.minimum_target
        achieved_sales = 0.0
        balance_amount = 0.0
        bonus_amount = 0.0
        
        if kpi_record:
            # minimum_target = kpi_record.minimum_target
            achieved_sales = kpi_record.total_sales
            balance_amount = minimum_target - achieved_sales
            bonus_amount = kpi_record.bonus_amount
            _logger.info('KPI Values: %s, %s, %s, %s', minimum_target, achieved_sales, balance_amount, bonus_amount)
        if search_value:
            domain += ['|'] * 8 + [
                ('name', 'ilike', search_value),
                ('partner_id.name', 'ilike', search_value),
                ('partner_id.phone', 'ilike', search_value),
                ('partner_id.email', 'ilike', search_value),
                ('user_id.name', 'ilike', search_value),
                ('order_number', 'ilike', search_value),
                ('order_link', 'ilike', search_value),
                ('instruction_sheet_link', 'ilike', search_value),
                ('service_type_id', 'ilike', search_value),
            ]
        _logger.info('Filtered Domain_________________________________________________________________: %s', domain)
        filtered_orders = orders.sudo().search(domain)
        total_count = len(filtered_orders)
        total_pages = math.ceil(total_count / per_page)
        final_orders = filtered_orders[offset:offset + per_page]
        pager = portal_pager(
            url="/sale/dashboard",
            url_args={'search': search_value},
            total=total_count,
            page=page,
            step=per_page,
            scope=5,
        )
        _logger.info('books_________________: %s', pager)
        def format_currency(value, is_bonus=False):
            currency_symbol = request.env.company.currency_id.symbol if is_bonus else '$'
            return currency_symbol + ' ' + '{:,.2f}'.format(value)
        values = {
            'orders': final_orders,
            'total_sales': total_sales,
            'res_company': request.env.company,
            'current_status': status,
            'search_value': search_value,
            'page': page,
            'pager': pager,
            'total_pages': total_pages,
            'minimum_target': format_currency(minimum_target),
            'achieved_sales': format_currency(achieved_sales),
            'balance_amount': format_currency(balance_amount),
            'bonus_amount': format_currency(bonus_amount, is_bonus=True), 
            'minimum_target_raw': minimum_target,
            'achieved_sales_raw': achieved_sales,
            'balance_amount_raw': balance_amount,
            'bonus_amount_raw': bonus_amount,
        }
        _logger.info('books_________________: %s', values)
        return request.render('sales_portal_bdcalling.portal_sales_template', values)



    @http.route(['/sale/details'], type='http', auth="user", website=True)
    def quotation_form_update(self, **kw):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        if not employee:
            return request.redirect('/my')
        order_id = kw.get('order_id')
        if not order_id:
            return 'order_id not found'

        order_id = int(order_id)

        order = req.env['sale.order'].sudo().search([('id', '=', order_id)])
        
        if not order:
            return {'error': 'Order not found'}
        
        
        products = request.env['product.template'].sudo().search([
            ('portal_available', '=', True),            
        ])
        departments = request.env['hr.department'].sudo().search([])
        profiles = request.env['bd.profile'].sudo().search([])
        team_id = request.env['assign.team'].sudo().search([('company_id', '=', user.company_id.id)])
        partners = request.env['res.partner'].sudo().search([])
        # teams = request.env['assign.team'].sudo().search([('company_id', '=', user.company_id.id)])
        employees = request.env['hr.employee'].sudo().search([])
        mediums = request.env['bd.platform_source'].sudo().search([])
        sources = request.env['bd.order_source'].sudo().search([])
        tags = request.env['crm.tag'].sudo().search([])
        today = fields.Date.today().strftime('%Y-%m-%d')
        values = {
            'products': products,
            'departments': departments,
            'profiles': profiles,
            'mediums': mediums,
            'sources': sources,
            'partners': partners,
            'assign_team_id': team_id,
            # 'teams': teams,
            'tags': tags,
            'employees': employees,
            'employee': employee,
            'today': today,
            'order': order,
        }
        return request.render('sales_portal_bdcalling.portal_quotation_update_form', values)
    
    
    @http.route('/sale/update', type='json', auth='user', methods=['POST'], csrf=False)
    def update_sale_order(self, **kwargs):
        order_id = kwargs.get('order_id')
        if not order_id:
            return {'success': False, 'message': 'Missing order_id'}

        sale_order = request.env['sale.order'].sudo().browse(int(order_id))
        if not sale_order.exists():
            return {'success': False, 'message': 'Order not found'}

        def get_datetime(datetime_string):
            if not datetime_string:
                return False
            dt_object = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M")
            local_tz = pytz.timezone("Asia/Dhaka")
            local_dt = local_tz.localize(dt_object)
            utc_dt = local_dt.astimezone(pytz.utc)
            return utc_dt.strftime("%Y-%m-%d %H:%M:%S")

        # Convert incoming values
        partner_id = int(kwargs.get('partner_id')) if kwargs.get('partner_id') else False
        service_type_id = int(kwargs.get('service_type_id')) if kwargs.get('service_type_id') else False
        incoming_date = kwargs.get('incoming_date')
        delivery_last_date = get_datetime(kwargs.get('delivery_last_date'))
        amount = float(kwargs.get('amount')) if kwargs.get('amount') else False
        percentage = kwargs.get('percentage') if kwargs.get('percentage') else False
        charges_amount = float(kwargs.get('charges_amount')) if kwargs.get('charges_amount') else False
        delivery_amount = float(kwargs.get('delivery_amount')) if kwargs.get('delivery_amount') else False
        special_remarks = kwargs.get('special_remarks')
        order_status = kwargs.get('order_status')
        order_link = kwargs.get('order_link')
        instruction_sheet_link = kwargs.get('instruction_sheet_link')
        assign_team_id = int(kwargs.get('team_id')) if kwargs.get('team_id') else False
        sales_employee_id = int(kwargs.get('sales_employee_id')) if kwargs.get('sales_employee_id') else False
        order_number = kwargs.get('order_number')
        crm_tag_ids = kwargs.get('crm_tag_ids')
        if crm_tag_ids and isinstance(crm_tag_ids, str):
            crm_tag_ids = [int(tag) for tag in crm_tag_ids.split(',')]

        # Logging for debugging
        _logger.info('Received Data: %s', kwargs)
        _logger.info('Parsed crm_tag_ids: %s', crm_tag_ids)

        updates = {}

        if partner_id and sale_order.partner_id.id != partner_id:
            updates['partner_id'] = partner_id
        if service_type_id and sale_order.service_type_id.id != service_type_id:
            updates['service_type_id'] = service_type_id
        if incoming_date and sale_order.incoming_date != incoming_date:
            updates['incoming_date'] = incoming_date
        if delivery_last_date and sale_order.delivery_last_date != delivery_last_date:
            updates['delivery_last_date'] = delivery_last_date
        if amount and sale_order.amount != amount:
            updates['amount'] = amount
        if percentage and sale_order.percentage != percentage:
            updates['percentage'] = percentage
        if charges_amount and sale_order.charges_amount != charges_amount:
            updates['charges_amount'] = charges_amount
        if delivery_amount and sale_order.delivery_amount != delivery_amount:
            updates['delivery_amount'] = delivery_amount
        if special_remarks and sale_order.special_remarks != special_remarks:
            updates['special_remarks'] = special_remarks
        if order_status and sale_order.order_status != order_status:
            updates['order_status'] = order_status
        if order_link and sale_order.order_link != order_link:
            updates['order_link'] = order_link
        if order_number and sale_order.order_number != order_number:
            updates['order_number'] = order_number
        if instruction_sheet_link and sale_order.instruction_sheet_link != instruction_sheet_link:
            updates['instruction_sheet_link'] = instruction_sheet_link
        if assign_team_id and sale_order.assign_team_id.id != assign_team_id:
            updates['assign_team_id'] = assign_team_id
        if sales_employee_id and sale_order.employee_id.id != sales_employee_id:
            updates['sales_employee_id'] = sales_employee_id
        
        if crm_tag_ids and sorted([tag.id for tag in sale_order.crm_tag_ids]) != sorted(crm_tag_ids):
            updates['crm_tag_ids'] = [(6, 0, crm_tag_ids)]
        _logger.info('Updates to Apply: %s', updates)

        if updates:
            sale_order.write(updates)
            sale_order.message_post(body="Sale order updated by %s" % request.env.user.name)

            return {
                'success': True,
                'message': "Sale order updated successfully!",
            }
        else:
            return {
                'success': False,
                'message': "No changes detected.",
            }


    
    @http.route('/sale/get_sales_employee_info', type='json', auth='user')
    def get_sales_employee_info(self, emp_id):
        emp = request.env['hr.employee'].sudo().search([('barcode', '=', emp_id)], limit=1)
        
        if not emp:
            return {"success": False, "message": "Sales Employee not found"}

        return {
            "success": True,
            "employee_id": emp.id,
            "company": emp.company_id.name if emp.company_id else '',
            "name": emp.name if emp.name else '',
        }