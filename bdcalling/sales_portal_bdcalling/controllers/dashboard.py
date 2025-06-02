# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, request as req
from datetime import datetime, time, date, timedelta
from collections import defaultdict
import calendar
import logging
_logger = logging.getLogger(__name__)


class PortalDashboardUp(http.Controller):

    @http.route('/bdcalling/dashboard', type='http', auth="user", website=True)
    def portal_dashboard_update(self, **kw):
        # Global Variables
        user_id = req.env.user
        current_date = date.today()
        first_day_of_month = datetime(current_date.year, current_date.month, 1)
        a_now = datetime.now()
        a_year = a_now.year
        a_month = a_now.month

        last_day = calendar.monthrange(a_year, a_month)[1]

        print(f"The last day of the current month is: {last_day}")

        if last_day == 31:
            last_day_of_month = datetime(
                current_date.year, current_date.month, 1) - timedelta(days=1)
        else:
            last_day_of_month = datetime(
                current_date.year, current_date.month + 1, 1) - timedelta(days=1)

        first_day_of_month = first_day_of_month.replace(
            hour=0, minute=0, second=0)
        _logger.info('first_day_of_month: %s', first_day_of_month)
        last_day_of_month = last_day_of_month.replace(
            hour=23, minute=59, second=59)
        _logger.info('last_day_of_month: %s', last_day_of_month)
        total_order = req.env['sale.order'].sudo().search([
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('company_id', '=', user_id.company_id.id),
        ])
        _logger.info('total_order: %s', total_order)
        total_wip = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'wip'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('company_id', '=', user_id.company_id.id),
        ])
        _logger.info('total_wip: %s', total_wip)
        total_completed = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'complete'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('company_id', '=', user_id.company_id.id),

        ])
        _logger.info('total_completed: %s', total_completed)
        total_canceled = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'cancelled'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('company_id', '=', user_id.company_id.id),

        ])
        _logger.info('total_canceled: %s', total_canceled)
        total_nra = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'nra'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('company_id', '=', user_id.company_id.id),

        ])
        _logger.info('total_nra: %s', total_nra)
        total_revisions = req.env['sale.order'].sudo().search([
            ('order_status', '=', 'revisions'),
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('company_id', '=', user_id.company_id.id),

        ])

        """
        Best Sales Performer
        best_sales_performer
        """
        sales = req.env['sale.order'].sudo().search([
            ('date_order', '>=', first_day_of_month),
            ('date_order', '<=', last_day_of_month),
            ('order_status', 'not in', ('', 'cancelled')),
            ('company_id', '=', user_id.company_id.id),
        ])
        _logger.info('sales: %s', sales)
        best_sales = []
        for sale in sales:
            best_sale = [sale.sales_employee_id.id, sale.amount_total]
            best_sales.append(best_sale)

        sales_totals = defaultdict(float)

        for employee in best_sales:
            employee_id, amount = employee
            sales_totals[employee_id] += amount

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
            best_sale_d = [sale_d.delivered_assign_team_id.id, sale_d.amount_total]
            best_sales_delivered.append(best_sale_d)

        sales_totals_d = defaultdict(float)

        for team in best_sales_delivered:
            team_id, amount = team
            sales_totals_d[team_id] += amount

        best_team_id = None
        try:
            best_team_id = max(sales_totals_d, key=sales_totals_d.get)
        except ValueError:
            pass

        best_delivery_team_id = req.env['assign.team'].sudo().search(
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


        # Return values with proper handling for None values
        return req.render('sales_portal_bdcalling.dashboard_temp', {
            'total_order': total_order and len(total_order) or 0,
            'total_wip': total_wip and len(total_wip) or 0,
            'total_completed': total_completed and len(total_completed) or 0,
            'total_canceled': total_canceled and len(total_canceled) or 0,
            'total_nra': total_nra and len(total_nra) or 0,
            'total_revisions': total_revisions and len(total_revisions) or 0,
            'best_sale_performer': best_sale_performer or False,
            'best_delivery_team_id': best_delivery_team_id or False,

            # Purchase Requisition
            'total_pr_count': total_pr_count or 0,

            'total_dh_acc_count': total_dh_acc_count or 0,
            'total_it_acc_count': total_it_acc_count or 0,
            'total_ad_acc_count': total_ad_acc_count or 0,
            'total_scm_acc_count': total_scm_acc_count or 0,
            'total_fin_acc_count': total_fin_acc_count or 0,
            'total_ceo_acc_count': total_ceo_acc_count or 0,

            # Pending Purchase Requisition
            'total_dh_pen_count': total_dh_pen_count or 0,
            'total_it_pen_count': total_it_pen_count or 0,
            'total_ad_pen_count': total_ad_pen_count or 0,
            'total_scm_pen_count': total_scm_pen_count or 0,
            'total_fin_pen_count': total_fin_pen_count or 0,
            'total_ceo_pen_count': total_ceo_pen_count or 0,

            'purchase_access': purchase_access
        })
