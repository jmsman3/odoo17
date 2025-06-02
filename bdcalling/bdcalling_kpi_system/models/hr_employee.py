# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, timedelta
import logging
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    role_id = fields.Many2one('kpi.role', string='Role', store=True, domain="[('active', '=', True), ('company_id', '=', company_id)]")
    grade_id = fields.Many2one('kpi.grade', string='Grade',compute='_compute_role_id',store=True)
    minimum_target = fields.Float('Minimum Target',compute='_compute_role_id' , store=True)
    salary = fields.Float('Salary', store=True)

    @api.depends('salary','company_id','role_id')
    def _compute_role_id(self):
        for employee in self:
            grade = self.env['kpi.grade'].search([('role_id', '=', employee.role_id.id), ('active', '=', True),'&',('minimum_salary', '<=', employee.salary), ('maximum_salary', '>=', employee.salary),('company_id','=', employee.company_id.id)], limit=1)
            employee.grade_id = grade.id
            employee.minimum_target = grade.minimum_target
    
    
    def action_view_sales_achievements(self):
        self.ensure_one()
        return {
            'name': _('Sales Achievements'),
            'type': 'ir.actions.act_window',
            'res_model': 'employee.sales.achievement',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id}
        }
        
        
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        """Override to create KPI record when sale is confirmed"""
        result = super(SaleOrder, self).action_confirm()
        
        if self.sales_employee_id:
            try:
                self.env['employee.kpi'].create_kpi_record_from_sale(
                    self.sales_employee_id, 
                    self.amount_total,
                    self.incoming_date or fields.Date.context_today(self)
                )
                _logger.info('KPI record created/updated for employee %s from sale order %s', 
                            self.sales_employee_id.name, self.name)
            except Exception as e:
                _logger.error('Error creating KPI record from sale order %s: %s', self.name, e)
        
        return result

