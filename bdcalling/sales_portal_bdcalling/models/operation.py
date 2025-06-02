# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class EmployeeOrderDetails(models.Model):
    _name = 'project.operation'
    _description = 'Project Operation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee')
    employee_id_barcode = fields.Char(related='employee_id.barcode', string='Employee ID')
    employee_name = fields.Char(related='employee_id.name', string='Employee Name')
    user_id = fields.Many2one(related='employee_id.user_id', string='User ID')
    company_name = fields.Char(string='Company Name', related='employee_id.company_id.name')
    so_id = fields.Many2one('sale.order', string='Sale Order')
    date = fields.Date(string='Date')
    order_id = fields.Char(string='Order ID')
    project = fields.Char(string='Project')
    partner_id = fields.Many2one('res.partner', string='Partner')
    order_link = fields.Char(string='Order Link')
    order_status = fields.Selection([
        ('nra', 'NRA'),
        ('wip', 'WIP'),
        ('delivered', 'Delivered'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
        ('revisions', 'Revisions'),
        ('issues', 'Issues'),
    ], default='nra')    
    assigned_team_id = fields.Many2one('assign.team', string='Team')
    instruction_sheet_link = fields.Char(string='Instructions Sheet Link')
    # percentage = fields.Selection([
    #     ('0', '0'),
    #     ('3', '3'),
    #     ('5', '5'),
    #     ('10', '10'),
    #     ('20', '20'),
    # ],string='Percentage')
    percentage = fields.Integer(string='Percentage', default=0)

    delivery_amount = fields.Float(string='Delivery Amount')
    monetary_value = fields.Float(string='Monetary Value')
    revision_count = fields.Integer(string="Revision Count", default=0)

    special_remarks = fields.Text(string='Special Remarks')


    def write(self, vals):
        """Override to create KPI record when operation status changes to complete"""
        result = super(EmployeeOrderDetails, self).write(vals)
        
        if 'order_status' in vals and vals['order_status'] == 'complete':
            for operation in self:
                if operation.employee_id:
                    try:
                        self.env['employee.kpi'].create_kpi_record_from_sale(
                            operation.employee_id, 
                            operation.monetary_value,
                            operation.date or fields.Date.context_today(self)
                        )
                        _logger.info('KPI record created/updated for employee %s from operation %s', 
                                    operation.employee_id.name, operation.order_id)
                    except Exception as e:
                        _logger.error('Error creating KPI record from operation %s: %s', operation.order_id, e)
        
        return result