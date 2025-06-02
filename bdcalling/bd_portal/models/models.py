# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritResUser(models.Model):
    _inherit = 'res.partner'

    operation_manager = fields.Boolean()
    client_user_name = fields.Char(string='Client User ID')
    is_mp_customer = fields.Boolean(string='Marketplace Customer')
    mp_customer_fullname = fields.Char(string='Marketplace Customer Full Name')


class InheritProductTemplate(models.Model):
    _inherit = 'product.template'

    portal_available = fields.Boolean()
    is_purchase_requisition = fields.Boolean(string="Is Purchase Requisition", default=False)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    portal_available = fields.Boolean(related='product_tmpl_id.portal_available', store=True)
    is_purchase_requisition = fields.Boolean(string="Is Purchase Requisition",
                                             related='product_tmpl_id.is_purchase_requisition', store=True)


class InheritHrEmployee(models.Model):
    _inherit = 'hr.employee'

    user_id2 = fields.Many2one('res.users', string='User')
    is_all_sale = fields.Boolean(string='Access all sale in portal')


class InheritSale(models.Model):
    _inherit = 'sale.order'

    @api.constrains('order_number')
    def _check_unique_order_number(self):
        for record in self:
            if record.order_number:
                existing_order = self.search([('order_number', '=', record.order_number), ('id', '!=', record.id)])
                if existing_order:
                    raise ValidationError("The Order Number must be unique!")

    # Employee Details:
    employee_id = fields.Many2one('hr.employee',domain="[('company_id', '=', company_id)]")
    employee_id_barcode = fields.Char(related='employee_id.barcode')

    # Sales Employee Details:
    sales_employee_id = fields.Many2one('hr.employee',domain="[('company_id', '=', company_id)]")

    # Order details #
    # platform_source = fields.Selection([
    #     ('fiverr', 'Fiverr'),
    #     ('upwork', 'Upwork'),
    #     ('pph', 'PPH'),
    # ])
    platform_source_id = fields.Many2one('bd.platform_source')
    # order_source = fields.Selection([
    #     ('bid', 'Bid'),
    #     ('tips', 'Tips'),
    #     ('direct_order', 'Direct Order'),
    # ])

    order_source_id = fields.Many2one('bd.order_source')
    invoice_date = fields.Date(string='Invoice Date', compute='_compute_invoice_date', store=True)

    profile_id = fields.Many2one('bd.profile')
    client_user_id = fields.Many2one('res.partner')
    order_number = fields.Char()
    order_link = fields.Char()
    instruction_sheet_link = fields.Char()
    service_type_id = fields.Many2one('product.template', domain="[('portal_available', '=', True)]")
    incoming_date = fields.Date(default=lambda self: fields.Date.today())
    # delivery_last_date = fields.Date(default=lambda self: fields.Date.today())
    delivery_last_date = fields.Datetime()
    deadline = fields.Char()
    amount = fields.Float()
    charges_amount = fields.Float()
    delivery_amount = fields.Float()
    percentage = fields.Selection([
        ('0', '0'),
        ('3', '3'),
        ('5', '5'),
        ('10', '10'),
        ('20', '20'),
    ])
    special_remarks = fields.Text()

    # Project Information
    operation_employee_id = fields.Many2one('hr.employee')
    bd_team_id = fields.Many2one('bd.team')
    assigned_team_id = fields.Many2one('bd.team')
    delivered_team_id = fields.Many2one('bd.team')
    order_status = fields.Selection([
        ('nra', 'NRA'),
        ('wip', 'WIP'),
        ('delivered', 'Delivered'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
        ('revisions', 'Revisions'),
        ('issues', 'Issues'),
    ], default='nra')
    teams_delivery_date = fields.Date(string='Team\'s Delivery Date')

    crm_tag_ids = fields.Many2many('crm.tag')

    @api.onchange('amount', 'percentage')
    def _onchange_amount(self):
        amount = self.amount
        percentage = int(self.percentage)
        charges_amount = (percentage / 100) * amount  # 8.0
        delivery_amount = amount - charges_amount  # 72

        print("charges_amount:", charges_amount)
        print("delivery_amount:", delivery_amount)
        self.charges_amount = charges_amount
        self.delivery_amount = delivery_amount
    @api.depends('invoice_status', 'invoice_ids')
    def _compute_invoice_date(self):
        for order in self:
            posted_invoices = order.invoice_ids.filtered(lambda inv: inv.state == 'posted' and inv.invoice_date)
            if posted_invoices:
                order.invoice_date = posted_invoices[0].invoice_date
            else:
                order.invoice_date = False

    def _prepare_invoice(self):
        invoice_vals = super(InheritSale, self)._prepare_invoice()
        invoice_vals['employee_id'] = self.employee_id.id if self.employee_id else None
        invoice_vals['employee_id_barcode'] = self.employee_id_barcode
        invoice_vals['sales_employee_id'] = self.sales_employee_id.id if self.sales_employee_id else None
        # invoice_vals['platform_source'] = self.platform_source
        invoice_vals['platform_source_id'] = self.platform_source_id.id if self.platform_source_id else None
        invoice_vals['order_source_id'] = self.order_source_id.id if self.order_source_id else None
        invoice_vals['profile_id'] = self.profile_id.id if self.profile_id else None
        invoice_vals['client_user_id'] = self.client_user_id.id if self.client_user_id else None
        invoice_vals['order_number'] = self.order_number
        invoice_vals['incoming_date'] = self.incoming_date
        invoice_vals['delivery_last_date'] = self.delivery_last_date
        invoice_vals['percentage'] = self.percentage
        invoice_vals['operation_employee_id'] = self.operation_employee_id.id if self.operation_employee_id else None
        invoice_vals['assigned_team_id'] = self.assigned_team_id.id if self.assigned_team_id else None
        invoice_vals['delivered_team_id'] = self.delivered_team_id.id if self.delivered_team_id else None
        invoice_vals['order_status'] = self.order_status
        invoice_vals['teams_delivery_date'] = self.teams_delivery_date
        return invoice_vals


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    test = fields.Char()
    order = fields.Char()  # To avoid xml error

    # Employee Details:
    employee_id = fields.Many2one('hr.employee',domain="[('company_id', '=', company_id)]")
    employee_id_barcode = fields.Char(related='employee_id.barcode')

    # Sales Employee Details:
    sales_employee_id = fields.Many2one('hr.employee',domain="[('company_id', '=', company_id)]")
    sales_employee_id_barcode = fields.Char(related='sales_employee_id.barcode')
    # Order details #
    # platform_source = fields.Selection([
    #     ('fiverr', 'Fiverr'),
    #     ('upwork', 'Upwork'),
    #     ('pph', 'PPH'),
    # ])

    platform_source_id = fields.Many2one('bd.platform_source')
    order_source_id = fields.Many2one('bd.order_source')
    profile_id = fields.Many2one('bd.profile')
    client_user_id = fields.Many2one('res.partner')
    order_number = fields.Char()

    # order_link = fields.Char()
    # instruction_sheet_link = fields.Char()
    # service_type_id = fields.Many2one('product.template', domain="[('portal_available', '=', True)]")
    incoming_date = fields.Date()

    delivery_last_date = fields.Datetime()
    # deadline = fields.Char()
    # amount = fields.Float()
    # charges_amount = fields.Float()
    # delivery_amount = fields.Float()
    percentage = fields.Selection([
        ('0', '0'),
        ('3', '3'),
        ('5', '5'),
        ('10', '10'),
        ('20', '20'),
    ])
    # special_remarks = fields.Text()

    # Project Information
    operation_employee_id = fields.Many2one('hr.employee')
    # bd_team_id = fields.Many2one('bd.team')
    assigned_team_id = fields.Many2one('bd.team')
    delivered_team_id = fields.Many2one('bd.team')
    order_status = fields.Selection([
        ('nra', 'NRA'),
        ('wip', 'WIP'),
        ('delivered', 'Delivered'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
        ('revisions', 'Revisions'),
        ('issues', 'Issues'),
    ])
    teams_delivery_date = fields.Date(string='Team\'s Delivery Date')


class BdPlatform_source(models.Model):
    _name = 'bd.platform_source'
    _description = 'bd.platform_source'

    name = fields.Char()
    active = fields.Boolean(default=True)


class BdOrder_source(models.Model):
    _name = 'bd.order_source'
    _description = 'bd.order_source'

    name = fields.Char()
    active = fields.Boolean(default=True)


class BdTeam(models.Model):
    _name = 'bd.team'
    _description = 'bd.team'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)
    active = fields.Boolean(default=True)


class BdProfile(models.Model):
    _name = 'bd.profile'
    _description = 'bd.profile'

    platform_source_id = fields.Many2one('bd.platform_source', required=True)
    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)
    active = fields.Boolean(default=True)
