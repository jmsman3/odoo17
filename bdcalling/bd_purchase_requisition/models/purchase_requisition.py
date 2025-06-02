# -*- coding: utf-8 -*-

from datetime import date, datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseReq(models.Model):
    _name = "cus.purchase.requisition"
    _description = 'Purchase Requisition'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id desc'

    priority = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ])

    name = fields.Char(string='Name', copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    req_from = fields.Selection([('admin', 'Admin'), ('it', 'IT')],
                                string='Requisition From', tracking=True, copy=False, index=True, required=True)
    order_line_ids = fields.One2many('requisition.order.line', 'requisition_id', string='Requisition Order Lines', tracking=True)
    po_id = fields.Many2many('purchase.order', string='Purchase Order', tracking=True)
    picking_type_id = fields.Many2one('stock.picking.type', string='Delivered To',
                                      domain=[('sequence_code', '=', 'IN')], tracking=True)
    price_total = fields.Float(string='Total Price', compute='_compute_total_price')
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted'), ('approve_hr', 'Approved (HR)'),
                              ('approve_finance', 'Approved (Finance)'), ('approve_scm', 'Approved (SCM)'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], readonly=True,
                             default='draft', copy=False, string="Status", tracking=True)
    req_date = fields.Date(string='Date', default=fields.Date.context_today, required=True, copy=False, tracking=True)
    # req_done = fields.Boolean('Requisition Done', compute='_compute_req_done')
    user_id = fields.Many2one('res.users', string='Purchase Representative',
                              default=lambda self: self.env.user, readonly=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True, tracking=True)
    department = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', tracking=True)
    job_id = fields.Many2one('hr.job', string='Designation', related='employee_id.job_id', tracking=True)
    purchase_count = fields.Integer(string='Purchase', compute='_compute_purchase_count', tracking=True)

    def action_create_purchase(self):
        self.ensure_one()
        date = datetime.now()
        if not self.order_line_ids:
            raise UserError(_('Please add some products to create a purchase order.'))

        customer = self.employee_id.user_id

        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.employee_id.user_id2.partner_id.id,
            'pur_req_id': self.id,
            'date_order': date.today(),
            'user_id': self.user_id.id,
            'company_id': self.company_id.id,
            'state': 'draft',
        })
        for line in self.order_line_ids:
            po_line_vals = self.env['purchase.order.line']._prepare_purchase_order_line(
                line.product_id,
                line.quantity,
                line.uom_id,
                line.company_id,
                customer,
                purchase_order,
            )
            new_po_line = self.env['purchase.order.line'].create(po_line_vals)
            line.purchase_order_line_id = new_po_line.id
            purchase_order.order_line = [(4, new_po_line.id)]


    @api.depends('po_id')
    def _compute_purchase_count(self):
        for rec in self:
            po = self.env['purchase.order'].search([('pur_req_id', '=', rec.id)])
            if po:
                rec.purchase_count = len(po)
            elif rec.po_id:
                rec.purchase_count = len(rec.po_id)
            else:
                rec.purchase_count = 0

    def action_view_purchase(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Orders'),
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('pur_req_id', '=', self.id)],
        }

    # Department Approvals
    is_department_head = fields.Boolean(string='Department Head', tracking=True)
    approval_date_department_head = fields.Date(string='Accept/Cancel Date (Dept. Head)', tracking=True)
    is_it_department = fields.Boolean(string='It Department', tracking=True)
    approval_date_it_department = fields.Date(string='Accept/Cancel Date (It Dept.)', tracking=True)
    is_admin_department = fields.Boolean(string='Admin Department', tracking=True)
    approval_date_admin_department = fields.Date(string='Accept/Cancel Date (Admin Dept.)', tracking=True)
    is_finance_department = fields.Boolean(string='Finance Department', tracking=True)
    approval_date_finance_department = fields.Date(string='Accept/Cancel Date (Finance)', tracking=True)
    is_scm_department = fields.Boolean(string='SCM Department', tracking=True)
    approval_date_scm_department = fields.Date(string='Accept/Cancel Date (SCM)', tracking=True)
    approval_date_ceo = fields.Date(string='Accept/Cancel Date (CEO)', tracking=True)

    team_id = fields.Many2one('bd.team')
    quantity = fields.Integer()
    deadline = fields.Date()
    purpose_of_use = fields.Char()

    app_state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approve_dh', 'Approved (Dept. Head)'),
        ('cancel_dh', 'Cancel (Dept. Head)'),
        ('approve_it', 'Approved (It Dept.)'),
        ('cancel_it', 'Cancel (It Dept.)'),
        ('approve_admin', 'Approved (Admin Dept.)'),
        ('cancel_admin', 'Cancel (Admin Dept.)'),
        ('approve_scm', 'Approved (SCM)'),
        ('cancel_scm', 'Cancel (SCM)'),
        ('approve_finance', 'Approved (Finance)'),
        ('cancel_finance', 'Cancel (Finance)'),
        ('approve_ceo', 'Approved (CEO)'),
        ('cancel_ceo', 'Cancel (CEO)'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default='draft', copy=False, string="Approval State", tracking=True)

    item_category = fields.Selection([
        ('admin', 'Admin'),
        ('it', 'It'),
    ])

    item_name = fields.Char()
    item_description = fields.Text()

    attachment_ids = fields.Many2many('bd.req.attachment', domain=[
        ('res_model', '=', 'cus.purchase.requisition')
    ], string='Requisition Attachments')

    # bd.req.attachment

    alternative_products = fields.Char()
    alternative_product_file_ids = fields.Many2many('bd.file', domain=[
        ('res_model', '=', 'cus.purchase.requisition')
    ], string='Alt. Pd. Attachments')

    department_head_state = fields.Selection([
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
    ], string='Dep. Head State')
    it_department_state = fields.Selection([
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
    ], string='It Dep. State')
    admin_department_state = fields.Selection([
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
    ], string='Admin Dep. State')
    scm_department_state = fields.Selection([
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
    ], string='SCM Dep. State')
    finance_department_state = fields.Selection([
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
    ], string='Finance Dep. State')
    ceo_state = fields.Selection([
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
    ], string='CEO State')

    company_id = fields.Many2one('res.company')
    purchase_id = fields.Many2one('purchase.order')

    budget = fields.Float()
    budget_pass_date = fields.Date()

    def action_approve_dh(self):
        self.write({'app_state': 'approve_dh',
                    'approval_date_department_head': date.today(),
                    'department_head_state': 'accepted',
                    })

    def action_cancel_dh(self):
        self.write({'app_state': 'cancel_dh',
                    'approval_date_department_head': date.today(),
                    'department_head_state': 'canceled',
                    })

    def action_approve_it(self):
        self.write({'app_state': 'approve_it',
                    'approval_date_it_department': date.today(),
                    'it_department_state': 'accepted',
                    })

    def action_cancel_it(self):
        self.write({'app_state': 'cancel_it',
                    'approval_date_it_department': date.today(),
                    'it_department_state': 'canceled',
                    })

    def action_approve_admin(self):
        self.write({'app_state': 'approve_admin',
                    'approval_date_admin_department': date.today(),
                    'admin_department_state': 'accepted',
                    })

    def action_cancel_admin(self):
        self.write({'app_state': 'cancel_admin',
                    'approval_date_admin_department': date.today(),
                    'admin_department_state': 'canceled',
                    })

    def action_approve_scm(self):
        self.write({'app_state': 'approve_scm',
                    'approval_date_scm_department': date.today(),
                    'scm_department_state': 'accepted',
                    })

    def action_cancel_scm(self):
        self.write({'app_state': 'cancele_scm',
                    'approval_date_scm_department': date.today(),
                    'scm_department_state': 'canceled',
                    })

    def action_approve_finance(self):
        self.write({'app_state': 'approve_finance',
                    'approval_date_finance_department': date.today(),
                    'finance_department_state': 'accepted',
                    })

    def action_cancel_finance(self):
        self.write({'app_state': 'cancel_finance',
                    'approval_date_finance_department': date.today(),
                    'finance_department_state': 'canceled',
                    })

    def action_approve_ceo(self):
        self.write({'app_state': 'approve_ceo',
                    'approval_date_ceo': date.today(),
                    'ceo_state': 'accepted',
                    })

    def action_cancel_ceo(self):
        self.write({'app_state': 'cancel_ceo',
                    'approval_date_ceo': date.today(),
                    'ceo_state': 'canceled',
                    })

    def action_done(self):
        self.write({'app_state': 'done'})

    def action_cancel(self):
        self.write({'app_state': 'cancel'})

    def action_draft(self):
        self.write({'app_state': 'draft'})


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'purchase.req.sequence') or _('New')

        res = super(PurchaseReq, self).create(vals)
        return res


class RequisitionLine(models.Model):
    _name = "requisition.order.line"

    requisition_id = fields.Many2one('cus.purchase.requisition', string='Purchase Requisition No')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1)
    purchase_qty = fields.Float(string='Purchased Qty', compute='_compute_pur_qty')
    pur_remaining_qty = fields.Float(string='Remaining Qty', compute='_compute_pur_qty')
    uom_id = fields.Many2one('uom.uom', 'UoM')
    price_unit = fields.Float(string='Unit Price', related='product_id.standard_price')
    price_subtotal = fields.Float(string='Subtotal Price', compute='_compute_subtotal_price')
    name = fields.Char(string='Description')
    purpose_of_use = fields.Char(string='Purpose of Use')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id')
    purchase_order_line_id = fields.Many2one('purchase.order.line', string='Purchase Order Line')


    @api.depends('quantity', 'price_unit')
    def _compute_subtotal_price(self):
        for rec in self:
            rec.price_subtotal = rec.quantity * rec.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                rec.uom_id = rec.product_id.uom_po_id.id

    @api.depends('requisition_id')
    def _compute_pur_qty(self):
        for rec in self:
            rec.purchase_qty = 0
            rec.pur_remaining_qty = 0
            pur_lines = self.env['purchase.order.line'].search(
                [('product_id', '=', rec.product_id.id), ('pur_req_id', '=', rec.requisition_id.id),
                 ('parent_state', '=', 'purchase')])
            print("pur_lines: ", pur_lines)
            qty = 0
            for record in pur_lines:
                product = record.product_id.name
                qty = qty + record.product_qty

            rec.purchase_qty = qty
            rec.pur_remaining_qty = rec.quantity - rec.purchase_qty


class BdFile(models.Model):
    _name = "bd.file"

    name = fields.Char()
    file = fields.Binary(string='File', required=True)
    res_model = fields.Char()
    res_id = fields.Integer()


class BdReqAttachment(models.Model):
    _name = "bd.req.attachment"

    name = fields.Char()
    file = fields.Binary(string='File', required=True)
    res_model = fields.Char()
    res_id = fields.Integer()



