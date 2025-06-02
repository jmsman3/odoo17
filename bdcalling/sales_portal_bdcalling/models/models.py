# -*- coding: utf-8 -*-

from odoo import models, fields, api


class saleOrderInherit(models.Model):
    _inherit = 'sale.order'
    
    deadline = fields.Char(string='Deadline')
    assign_team_id = fields.Many2one('assign.team', string="Assign Team")
    delivered_assign_team_id = fields.Many2one('assign.team', string="Delivered Team")

