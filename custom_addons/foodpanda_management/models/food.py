from odoo import api, fields, models
from odoo.exceptions import ValidationError 
from datetime import timedelta

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
    
    
    #Constraint er kaaj holo Validation Handel kora
    @api.constrains('quantity','price_per_unit')
    def checking_quanity_valid_or_not(self):
        if self.quantity <=0:
            raise ValidationError("Quantity must be greater than Zero")
        if self.price_per_unit <=0:
            raise ValidationError("Price per Unit Must be Greater than Zero")
    
    # @api.constrains('order_date_and_time')
    # def check_order_date_future_or_not(self):

    #     print("----------------------------------------------------------------------")
    #     print("Date only......." , self)
    #     print("----------------------------------------------------------------------")

    #     if self.order_date_and_time > fields.Datetime.now():
    #         raise ValidationError("Order date time cannot be in future")
    #     else:
    #         pass
        
    #     #CHecking order date is toooo old(# 30 din er besi hole error show kora lagbe)
    #     date_storing_withn_30_days_ago = fields.datetime.now() - timedelta(days=30)
    #     if self.order_date_and_time < date_storing_withn_30_days_ago:
    #         raise ValidationError("Order date is too old. Must be within the last 30 days") 
    #     else:
    #         pass
        
    #     #Check SETup Order Must be deya lagbe 
    #     if not self.order_date_and_time:
    #         raise ValidationError("Order Date and Time Required")
    

    @api.constrains('order_date_and_time')
    def check_order_date_future_or_not(self):

        print("----------------------------------------------------------------------")
        print("Date only......." , self)
        print("----------------------------------------------------------------------")
        for record in self:
            # Order Date Required
            if not record.order_date_and_time:
                raise ValidationError("Order Date and Time Required")

            # Future date check
            if record.order_date_and_time > fields.Datetime.now():
                raise ValidationError("Order date time cannot be in future")

            # Too old date check
            date_30_days_ago = fields.Datetime.now() - timedelta(days=30)
            if record.order_date_and_time < date_30_days_ago:
                raise ValidationError("Order date is too old. Must be within the last 30 days")

        
        
    
    #THIS FUNCTION FOR DISCOUNT CALCULAION(Save data in Databse, if api depends) 
    @api.depends('quantity')
    def _compute_discount(self):
        if self.quantity>10:
            self.discount = 10
        else:
            self.discount = 0
        
    #This function for SET TOTAL PRICE(Do not saves data in Database, if api onchange use kora hoi)
    @api.onchange('total_price')
    def _compute_net_price(self):

        self.net_price = self.total_price * ( 1 - (self.discount/100.0))

    #THIS FUNCTION FOR Total Price CALCULAION(Save data in Databse, if api depends) 
    @api.depends('quantity','price_per_unit')
    def _compute_total_price(self):
        print("----------------------------------------------------------------------")
        print("Total price......." , self)
        print("----------------------------------------------------------------------")

        for record in self:
            record.total_price = record.quantity * record.price_per_unit
        
        # print("herrrrr selfff............", self)
        # print('\n')
        # print("herrrrr Total price............", self.total_price)
        # print("herrrrr quantity price............", self.quantity)
        # print("herrrrr price_per_unit price............", self.price_per_unit)
