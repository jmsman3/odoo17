from odoo import api, fields, models


class FoodPanda(models.Model):
    _name = 'food.order'
    _description= 'It is the best food ordering platform for customers'
    _inherit = ['mail.thread']
    _rec_name = 'customer_name' 

    customer_name = fields.Char(string="Customer name", required=True)
    food_item = fields.Char(string="Food item", required=True)
    quantity = fields.Integer(string="Quantity", default=1)
    price_per_unit = fields.Float(string="Price per Unit",required=True)

    order_date_and_time = fields.Datetime(string="Orders date and time", default=fields.Datetime.now)

    status = fields.Selection(
        [
            ('pending','Pending'),
            ('confirmed', 'Confirmed'),
            ('delivered', 'Delivered'),

        ],string="Order Status" ,default='pending'
    )
    
    chef_id = fields.Many2one('foodpanda.chef', string="Chef Assigned")

    total_price = fields.Float(string='Total Price' , compute='_compute_total_price')

    discount = fields.Float(string="Discount (%)", compute='_compute_discount')
    net_price = fields.Float(string="Net Price", compute="_compute_net_price")


    @api.depends('quantity')
    def _compute_discount(self):
        if self.quantity>10:
            self.discount = 10
        else:
            self.discount = 0
        
    #This function for SET TOTAL PRICE
    @api.onchange('total_price')
    def _compute_net_price(self):

        self.net_price = self.total_price * ( 1 - (self.discount/100.0))

    
    @api.depends('quantity','price_per_unit')
    def _compute_total_price(self):
       
        self.total_price = self.quantity * self.price_per_unit
        
        # print("herrrrr selfff............", self)
        # print('\n')
        # print("herrrrr Total price............", self.total_price)
        # print("herrrrr quantity price............", self.quantity)
        # print("herrrrr price_per_unit price............", self.price_per_unit)
