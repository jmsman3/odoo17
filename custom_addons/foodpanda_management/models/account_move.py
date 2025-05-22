from odoo import api , models , fields

class AccountMove(models.Model):
    _inherit = "account.move"

    appointment_id = fields.Many2one('food.order', string="Chef Appointment") #this line iherits the whole objects 

    
 



class AccountMoveLine(models.Model):
    _inherit  = "account.move.line"

    full_object = fields.Many2one('food.order' , string="Product Owner")
    food_item = fields.Char(related='full_object.food_item', string="Food name", store = True )




    
   