# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import logging
import calendar
_logger = logging.getLogger(__name__)


class EmployeeKpi(models.Model):
    _name = 'employee.kpi'
    _description = 'Employee KPI Assignment'
    _rec_name = 'employee_id'
    _order = 'period_end desc, id desc'
    
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    role_id = fields.Many2one('kpi.role', string='Role', required=True)
    grade_id = fields.Many2one('kpi.grade', string='Grade', required=True)
    minimum_target = fields.Float(related='grade_id.minimum_target', string='Minimum Target', readonly=True)
    
    period_start = fields.Date('Period Start', required=True, 
                              default=lambda self: date(fields.Date.context_today(self).year, 
                                                       fields.Date.context_today(self).month, 1) - relativedelta(months=1))
    period_end = fields.Date('Period End', required=True,
                            default=lambda self: date(fields.Date.context_today(self).year, 
                                                     fields.Date.context_today(self).month, 1) - relativedelta(days=1))
    total_sales = fields.Float('Total Operations', required=True, default=0.0)
    bonus_amount = fields.Float('Bonus Amount', required=True, default=0.0)
    shortfall_amount = fields.Float('Shortfall Amount', default=0.0, 
                                   help="Amount by which sales fell short of minimum target")
    is_penalty = fields.Boolean('Is Penalty', default=False, 
                               help="Indicates if this record represents a penalty for not meeting minimum target")
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid')
    ], string='Status', default='draft')
    
    @api.constrains('period_start', 'period_end')
    def _check_dates(self):
        for record in self:
            if record.period_start > record.period_end:
                raise ValidationError(_("Period start date cannot be after period end date."))
    
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
    
    def action_mark_paid(self):
        for record in self:
            record.state = 'paid'
    
    def action_reset_to_draft(self):
        for record in self:
            record.state = 'draft'
    
    def action_calculate_record(self):
        """Calculate/recalculate the current KPI record"""
        self.ensure_one()
        
        if self.state == 'paid':
            raise UserError(_("Cannot recalculate a record that has already been paid."))
        
        total_sales = self._get_employee_sales(self.employee_id, self.period_start, self.period_end)
        minimum_target = self.grade_id.minimum_target
        is_penalty = total_sales < minimum_target
        shortfall_amount = 0.0
        
        if is_penalty:
            shortfall_amount = minimum_target - total_sales
            bonus_amount = -shortfall_amount
        else:
            bonus_amount = self._calculate_bonus(self.employee_id, total_sales)
        
        self.write({
            'total_sales': total_sales,
            'bonus_amount': bonus_amount,
            'shortfall_amount': shortfall_amount,
            'is_penalty': is_penalty,
            'state': 'draft'
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Calculation Complete'),
                'message': _('KPI record for %s has been recalculated.') % self.employee_id.name,
                'sticky': False,
                'type': 'success',
                'next': {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                },
            },
        }
        
    
    @api.model
    def action_bulk_calculate(self):
        """Bulk calculate selected KPI records"""
        active_ids = self.env.context.get('active_ids', [])
        records = self.browse(active_ids)
        
        if not records:
            raise UserError(_("No records selected for calculation."))
        
        calculated_count = 0
        skipped_count = 0
        
        for record in records:
            if record.state == 'paid':
                skipped_count += 1
                continue
                
            total_sales = self._get_employee_sales(record.employee_id, record.period_start, record.period_end)
            
            minimum_target = record.grade_id.minimum_target
            
            is_penalty = total_sales < minimum_target
            shortfall_amount = 0.0
            
            if is_penalty:
                shortfall_amount = minimum_target - total_sales
                bonus_amount = -shortfall_amount
            else:
                bonus_amount = self._calculate_bonus(record.employee_id, total_sales)
            
            record.write({
                'total_sales': total_sales,
                'bonus_amount': bonus_amount,
                'shortfall_amount': shortfall_amount,
                'is_penalty': is_penalty,
                'state': 'draft'
            })
            
            calculated_count += 1
        
        message = _("%s records recalculated successfully.") % calculated_count
        if skipped_count > 0:
            message += _(" %s records were skipped because they were already paid.") % skipped_count
         
         
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Calculation Complete'),
                'message': message,
                'sticky': False,
                'type': 'success',
                'next': {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                },
            },
        }
        
    
    @api.model
    def calculate_monthly_bonus(self):
        """
        Cron job to calculate monthly bonus for all employees
        This runs on the first day of each month for the previous month
        If a record already exists for the period and the sales value has increased,
        update the existing record instead of creating a new one.
        If total sales is less than minimum target, apply penalty.
        """
        today = fields.Date.context_today(self)
        _logger.info('Calculating monthly bonus for %s', today)
        first_day_prev_month = date(today.year, today.month, 1) - relativedelta(months=1)
        last_day_prev_month = date(today.year, today.month, 1) - relativedelta(days=1)
        
        # Get all employees with roles assigned
        employees = self.env['hr.employee'].search([
            ('role_id', '!=', False),
            ('active', '=', True)
        ])
        _logger.info('Calculating monthly bonus for %s employees', len(employees))
        
        for employee in employees:
            if not employee.grade_id:
                _logger.info('Employee %s has no grade, skipping', employee.name)
                continue
                
            total_sales = self._get_employee_sales(employee, first_day_prev_month, last_day_prev_month)
            _logger.info('Employee %s total sales: %s', employee.name, total_sales)
            
            minimum_target = employee.grade_id.minimum_target
            
            is_penalty = total_sales < minimum_target
            shortfall_amount = 0.0
            
            if is_penalty:
                shortfall_amount = minimum_target - total_sales
                _logger.info('Employee %s has shortfall of %s (minimum target: %s)', 
                            employee.name, shortfall_amount, minimum_target)
            
            bonus_amount = self._calculate_bonus(employee, total_sales)
            
            if is_penalty:
                bonus_amount = -shortfall_amount
                _logger.info('Employee %s penalty amount: %s', employee.name, bonus_amount)
            else:
                _logger.info('Employee %s bonus amount: %s', employee.name, bonus_amount)
            
            # Check if a record already exists for this employee and period
            existing_record = self.env['employee.kpi'].search([
                ('employee_id', '=', employee.id),
                ('period_start', '=', first_day_prev_month),
                ('period_end', '=', last_day_prev_month)
            ], limit=1)
            
            if existing_record:
                pass
                should_update = False
                
                if is_penalty:
                    should_update = True
                else:
                    should_update = total_sales > existing_record.total_sales
                
                if should_update and existing_record.state != 'paid':
                    _logger.info('Updating existing KPI record for employee %s. Old sales: %s, New sales: %s', 
                                employee.name, existing_record.total_sales, total_sales)
                    try:
                        existing_record.write({
                            'total_sales': total_sales,
                            'bonus_amount': bonus_amount,
                            'shortfall_amount': shortfall_amount,
                            'is_penalty': is_penalty,
                            # Reset to draft if it was confirmed but values changed
                            'state': 'draft' if existing_record.state == 'confirmed' else existing_record.state
                        })
                        _logger.info('KPI record updated for employee %s', employee.name)
                    except Exception as e:
                        _logger.error('Error updating KPI record for employee %s: %s', employee.name, e)
                else:
                    _logger.info('No update needed for employee %s KPI record', employee.name)
            else:
                # Create new KPI record if none exists
                try:
                    self.create({
                        'employee_id': employee.id,
                        'role_id': employee.role_id.id,
                        'grade_id': employee.grade_id.id,
                        'period_start': first_day_prev_month,
                        'period_end': last_day_prev_month,
                        'total_sales': total_sales,
                        'bonus_amount': bonus_amount,
                        'shortfall_amount': shortfall_amount,
                        'is_penalty': is_penalty,
                        'state': 'draft'
                    })
                    _logger.info('New KPI record created for employee %s', employee.name)
                except Exception as e:
                    _logger.error('Error creating KPI record for employee %s: %s', employee.name, e)
            
        return True
    
    def _get_employee_sales(self, employee, start_date, end_date):
        """Calculate total sales for an employee in the given period"""
        try:
            sales_orders = self.env['sale.order'].sudo().search([
                ('sales_employee_id', '=', employee.id),
                ('incoming_date', '>=', start_date),
                ('incoming_date', '<=', end_date),
                ('state', 'in', ['sale', 'done'])
            ])
            _logger.info('Employee %s sales orders: %s', employee.name, len(sales_orders))
            if sales_orders:            
                return sum(sales_orders.mapped('amount_total'))
            else:
                operations = self.env['project.operation'].sudo().search([
                    ('employee_id', '=', employee.id),
                    ('date', '>=', start_date),
                    ('date', '<=', end_date),
                    ('order_status', '=', 'complete')])
                _logger.info('Employee %s operations: %s', employee.name, len(operations))
                return sum(operations.mapped('monetary_value'))
        except Exception as e:
            _logger.error('Error calculating sales for employee %s: %s', employee.name, e)
            return 0.0
    
    def _calculate_bonus(self, employee, total_sales):
        """Calculate bonus amount based on employee's grade and total sales"""
        try:
            if total_sales < employee.grade_id.minimum_target:
                return 0.0
            _logger.info(f"to find level---------------{employee.grade_id.name}----{total_sales}---{employee.company_id.name}")
            level = self.env['kpi.level'].search([
                ('grade_id', '=', employee.grade_id.id),
                ('min_amount', '<=', total_sales),
                ('max_amount', '>', total_sales),
                ('company_id','=', employee.company_id.id),
            ], limit=1)
            _logger.info(f"level______________________1{level}")

            if not level:
                level = self.env['kpi.level'].search([
                ('grade_id', '=', employee.grade_id.id),
                ('min_amount', '<=', total_sales),
                ('max_amount', '=', 0),
                ('company_id','=', employee.company_id.id),
            ], limit=1)
            _logger.info(f"level______________________2{level}")
            if level:
                _logger.info('Employee %s matched level %s with bonus %s', 
                            employee.name, level.name, level.bonus_amount)
                return level.bonus_amount
            else:
                _logger.info('No matching level found for employee %s with sales %s', 
                            employee.name, total_sales)
                return 0.0
        except Exception as e:
            _logger.error('Error calculating bonus for employee %s: %s', employee.name, e)
            return 0.0
        
        
    
    @api.model
    def create_kpi_record_from_sale(self, employee, amount, date_completed):
        """
        Create or update a KPI record when a sale or operation is completed
        
        Args:
            employee: hr.employee record
            amount: float, the amount of the sale/operation
            date_completed: date when the sale/operation was completed
        """
        if not employee or not employee.role_id or not employee.grade_id:
            _logger.warning('Cannot create KPI record: Employee %s has no role or grade assigned', 
                          employee.name if employee else 'None')
            return False
            
        period_start = date(date_completed.year, date_completed.month, 1)
        last_day = calendar.monthrange(date_completed.year, date_completed.month)[1]
        period_end = date(date_completed.year, date_completed.month, last_day)
        
        existing_record = self.env['employee.kpi'].search([
            ('employee_id', '=', employee.id),
            ('period_start', '=', period_start),
            ('period_end', '=', period_end)
        ], limit=1)
        
        total_sales = self._get_employee_sales(employee, period_start, period_end)
        
        minimum_target = employee.grade_id.minimum_target
        
        is_penalty = total_sales < minimum_target
        shortfall_amount = 0.0
        
        if is_penalty:
            shortfall_amount = minimum_target - total_sales
            bonus_amount = -shortfall_amount
        else:
            bonus_amount = self._calculate_bonus(employee, total_sales)
        
        if existing_record:
            if existing_record.state != 'paid':
                _logger.info('Updating existing KPI record for employee %s. New total sales: %s', 
                            employee.name, total_sales)
                existing_record.write({
                    'total_sales': total_sales,
                    'bonus_amount': bonus_amount,
                    'shortfall_amount': shortfall_amount,
                    'is_penalty': is_penalty,
                    'state': 'draft' if existing_record.state == 'confirmed' else existing_record.state
                })
        else:
            # Create new KPI record
            _logger.info('Creating new KPI record for employee %s with sales: %s', employee.name, total_sales)
            self.create({
                'employee_id': employee.id,
                'role_id': employee.role_id.id,
                'grade_id': employee.grade_id.id,
                'period_start': period_start,
                'period_end': period_end,
                'total_sales': total_sales,
                'bonus_amount': bonus_amount,
                'shortfall_amount': shortfall_amount,
                'is_penalty': is_penalty,
                'state': 'draft'
            })
        
        return True

