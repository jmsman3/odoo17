from odoo import models, fields,api

class TravelManagement(models.Model):
    # Model Purpose likte hobe
    _name = "travel.management"
    _inherit = ['mail.thread']
    _description = "Travel"
    

    name = fields.Char(string='Name',required=True)
    employee_id = fields.Char(string='Employee ID')
    destination = fields.Char(string="Destination")
    departure_date = fields.Date(string="Departure Date")
    return_date = fields.Date(string="Return Date")
    travel_mode = fields.Selection([
        ('air', 'Air'),
        ('train','Train'),
        ('bus','Bus'),
        ('other','Other'),
    ], string="Travel Mode", required=True)
    ticket_number = fields.Char(string="Ticket Number")
    hotel_booking = fields.Boolean(string="Hotel Booking")
    hotel_name = fields.Char(string='Hotel Name')



    @api.model
    def create(self,vals):
        print('Creating a new customer:', vals.get('name'))
        # print('self', self.get('name'))
        print('Creating a new travel:', vals.get('name'))
        return super().create(vals)

  

