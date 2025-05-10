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


    #This function for SET TOTAL PRICE
    @api.depends('quantity','price_per_unit')
    def _compute_total_price(self):
        for i in self:
            i.total_price = i.quantity * i.price_per_unit
    
    @api.depends('quantity')
    def _compute_discount(self):
        for j in self:
            if j.quantity > 10:
                j.discount = 10.0
            else:
                j.discount = 0.0
    
    @api.onchange('total_price')
    def _compute_net_price(self):
        for k in self:
            k.net_price = k.total_price * ( 1 - (k.discount/100.0))

    

