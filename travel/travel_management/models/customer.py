

from odoo import models, fields

class Customer(models.Model):
    # Customer information model
    

    _name = "customer.info"
    _inherit = ['mail.thread']
    _description = "Customer Info"
    

    name = fields.Char(string='Name',required=True)
    email = fields.Char(string='Email')
    phone = fields.Integer(string="Phone")
    address = fields.Char(string='Address')
    date_of_birth = fields.Date(string='DOB')
    gender = fields.Selection([('male','Male'), ('female','Female')], string='Gender')




# compute field database heavy kore eta skip kora vlo


