# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class InheritResUser(models.Model):
    _inherit = 'res.users'

    department_head = fields.Boolean()
    category = fields.Selection([
        ('it', 'It'),
        ('admin', 'Admin'),
    ])

    # For it dept. only
    it_department = fields.Boolean()

    # For all dept.
    admin_department = fields.Boolean()
    finance_department = fields.Boolean()
    scm_department = fields.Boolean()
    is_ceo = fields.Boolean()

    can_create_sale = fields.Boolean(string='Can Create Sale')
    is_project_manager = fields.Boolean(string='Project Manager')

# _________________________________________RAYTA____________________________________________________

    sale_leader = fields.Boolean(string='Sale Leader')
    sales_man = fields.Boolean(string='Sales Man')
    operation_leader = fields.Boolean(string='Operation Leader')
    operation_man = fields.Boolean(string='Operation Man')
    bus_dev = fields.Boolean(string='Business Development')
    
    
    
class AssignTeam(models.Model):
    _name = 'assign.team'
    _description = 'Assign Team'
    
    name = fields.Char(string='Name', required=True)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('hr.employee', 'assign_team_id', string='Team Members')
    company_id = fields.Many2one('res.company', string='Company')



class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    assign_team_id = fields.Many2one('assign.team', string='Assign Team', help='Team assigned to the employee')

    @api.constrains('assign_team_id', 'company_id')
    def _check_team_company(self):
        for employee in self:
            if employee.assign_team_id and employee.company_id and employee.assign_team_id.company_id != employee.company_id:
                raise ValidationError(_("The assigned team must belong to the same company as the employee."))