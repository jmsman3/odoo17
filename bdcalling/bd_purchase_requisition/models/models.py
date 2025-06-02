# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BdNotification(models.Model):
    _name = 'bd.notification'
    _description = 'bd.notification'
    _order = 'id desc'

    name = fields.Char()
    mark_as_read = fields.Boolean()
    employee_id = fields.Many2one('hr.employee')
    user_id = fields.Many2one('res.users')
    req_id = fields.Many2one('cus.purchase.requisition')
    department = fields.Selection([
        ('head', 'Department Head'),
        ('it', 'It Department'),
        ('admin', 'Admin Department'),
        ('scm', 'SCM Department'),
        ('finance', 'Finance Department'),
        ('ceo', 'CEO'),
    ])

