from odoo import api, fields, models


class FoodPanda(models.Model):
    _name = 'food.order'
    _description= 'It is the best food ordering platform for customers'
    _inherit = ['mail.thread']

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

    @api.depends('quantity','price_per_unit')
    def _compute_total_price(self):
        for jubaer in self:
            jubaer.total_price = jubaer.quantity * jubaer.price_per_unit
