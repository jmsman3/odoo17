from odoo import api , models , fields

class AccountMove(models.Model):
    _inherit = "account.move"

    appointment_id = fields.Many2one('food.order', string="Appointment")

        
    
    
    