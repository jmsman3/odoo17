# -*- coding: utf-8 -*-

from odoo import models, fields, api

class manufacture_employee_cost(models.Model):
    _name = 'manufacture_employee_cost.manufacture_employee_cost'
    _description = 'manufacture_employee_cost.manufacture_employee_cost'
    _inherit = 'mrp.workcenter'
    # workcenter_ids = fields.Many2many('mrp.workcenter', 'workcenter_employee_cost_rel', 'employee_cost_id', 'workcenter_id')


    name = fields.Char(string="Notun Field") 
   