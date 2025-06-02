# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class BonusCalculation(models.Model):
    _name = 'bonus.calculation'
    _description = 'Bonus Calculation'
    _order = 'date desc, id desc'
    
    name = fields.Char('Reference', required=True, copy=False, readonly=True, 
                       default=lambda self: _('New'))
    date = fields.Date('Calculation Date', default=fields.Date.context_today, required=True)
    period_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly')
    ], string='Period Type', default='monthly', required=True)
    period_start = fields.Date('Period Start', required=True)
    period_end = fields.Date('Period End', required=True)
    employee_ids = fields.Many2many('hr.employee', string='Employees')
    line_ids = fields.One2many('bonus.calculation.line', 'calculation_id', string='Calculation Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('calculated', 'Calculated'),
        ('approved', 'Approved'),
        ('paid', 'Paid')
    ], string='Status', default='draft', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('bonus.calculation') or _('New')
        return super(BonusCalculation, self).create(vals)
    
    @api.onchange('period_type', 'date')
    def _onchange_period_type(self):
        if self.period_type and self.date:
            if self.period_type == 'monthly':
                self.period_start = date(self.date.year, self.date.month, 1)
                self.period_end = (self.period_start + relativedelta(months=1, days=-1))
            elif self.period_type == 'quarterly':
                quarter = ((self.date.month - 1) // 3) + 1
                self.period_start = date(self.date.year, (quarter - 1) * 3 + 1, 1)
                self.period_end = (self.period_start + relativedelta(months=3, days=-1))
            elif self.period_type == 'yearly':
                self.period_start = date(self.date.year, 1, 1)
                self.period_end = date(self.date.year, 12, 31)
    
    def action_calculate_bonus(self):
        self.ensure_one()
        self.line_ids.unlink()
        
        domain = [
            ('date', '>=', self.period_start),
            ('date', '<=', self.period_end),
            ('state', '=', 'confirmed')
        ]
        
        if self.employee_ids:
            domain.append(('employee_id', 'in', self.employee_ids.ids))
        
        achievements = self.env['employee.sales.achievement'].search(domain)
        
        # Group by employee
        employee_achievements = {}
        for achievement in achievements:
            if achievement.employee_id.id not in employee_achievements:
                employee_achievements[achievement.employee_id.id] = {
                    'employee': achievement.employee_id,
                    'total_sales': 0.0,
                    'achievements': []
                }
            
            employee_achievements[achievement.employee_id.id]['total_sales'] += achievement.amount
            employee_achievements[achievement.employee_id.id]['achievements'].append(achievement)
        
        # Create calculation lines
        for emp_id, data in employee_achievements.items():
            employee = data['employee']
            total_sales = data['total_sales']
            
            # Get the employee's KPI assignment for the end of the period
            kpi_assignment = self.env['employee.kpi'].search([
                ('employee_id', '=', employee.id),
                ('start_date', '<=', self.period_end),
                '|',
                ('end_date', '=', False),
                ('end_date', '>=', self.period_end)
            ], limit=1)
            
            _logger.info(f"level______________________{kpi_assignment}")
            if not kpi_assignment:
                continue
            
            # Find the applicable level based on total sales
            level = self.env['kpi.level'].search([
                ('grade_id', '=', kpi_assignment.grade_id.id),
                ('min_amount', '<=', total_sales),
                ('max_amount', '>=', total_sales)
            ], limit=1)
            _logger.info(f"level______________________{level}")
            
            bonus_amount = level.bonus_amount if level else 0.0
            _logger.info(f"level______________________{bonus_amount}")
            
            # Create calculation line
            self.env['bonus.calculation.line'].create({
                'calculation_id': self.id,
                'employee_id': employee.id,
                'role_id': kpi_assignment.role_id.id,
                'grade_id': kpi_assignment.grade_id.id,
                'minimum_target': kpi_assignment.minimum_target,
                'total_sales': total_sales,
                'bonus_amount': bonus_amount,
                'achievement_ids': [(6, 0, [a.id for a in data['achievements']])]
            })
        
        self.state = 'calculated'
        return True
    
    def action_approve(self):
        self.ensure_one()
        self.state = 'approved'
        return True
    
    def action_mark_paid(self):
        self.ensure_one()
        self.state = 'paid'
        # Mark all related achievements as paid
        for line in self.line_ids:
            line.achievement_ids.write({'state': 'paid'})
        return True
    
    def action_reset_to_draft(self):
        self.ensure_one()
        self.state = 'draft'
        return True

class BonusCalculationLine(models.Model):
    _name = 'bonus.calculation.line'
    _description = 'Bonus Calculation Line'
    
    calculation_id = fields.Many2one('bonus.calculation', string='Calculation', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    role_id = fields.Many2one('kpi.role', string='Role', required=True)
    grade_id = fields.Many2one('kpi.grade', string='Grade', required=True)
    minimum_target = fields.Float('Minimum Target', required=True)
    total_sales = fields.Float('Total Sales', required=True)
    bonus_amount = fields.Float('Bonus Amount', required=True)
    achievement_ids = fields.Many2many('employee.sales.achievement', string='Achievements')
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.employee_id.name} - {record.bonus_amount}"
            result.append((record.id, name))
        return result
    
    
    

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _create_sales_achievement(self):
        _logger.info("Creating sales achievement for order %s", self.name)
        """Create sales achievement record when order is confirmed"""
        for order in self:
            if order.employee_id and order.amount_total > 0:
                self.env['employee.sales.achievement'].create({
                    'employee_id': order.employee_id.id,
                    'date': fields.Date.context_today(self),
                    'amount': order.amount_total,
                    'sale_order_id': order.id,
                    'state': 'draft'
                })
    
    def action_confirm(self):
        """Override to create sales achievement when order is confirmed"""
        _logger.info("Creating sales achievement for order %s", self.name)
        result = super(SaleOrder, self).action_confirm()
        self._create_sales_achievement()
        return result