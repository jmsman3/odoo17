# # my_module.py
# from odoo import models, fields, api

# # Model: Chef
# class Chef(models.Model):
#     _name = 'food.chef'
#     _description = 'Chef Info'

#     name = fields.Char(string='Name')
#     specialty = fields.Char(string='Specialty')
#     active = fields.Boolean(default=True)
#     food_ids = fields.One2many('food.item', 'chef_id', string='Food Items')


# # Model: FoodItem
# class FoodItem(models.Model):
#     _name = 'food.item'
#     _description = 'Food Item Info'

#     name = fields.Char(string='Food Name')
#     price = fields.Float(string='Price')
#     is_veg = fields.Boolean(string='Is Vegetarian')
#     chef_id = fields.Many2one('food.chef', string='Chef')


# # ORM Operations
# def orm_operations(env):
#     # 1. Create Chef
#     chef = env['food.chef'].create({'name': 'Chef Rahim', 'specialty': 'BBQ'})
#     print(f"Chef Created: {chef.name}")

#     # 2. Create Food Item
#     food = env['food.item'].create({
#         'name': 'Grilled Chicken',
#         'price': 300,
#         'is_veg': False,
#         'chef_id': chef.id
#     })
#     print(f"Food Created: {food.name}, Price: {food.price}")

#     # 3. Search Non-Veg Foods
#     foods = env['food.item'].search([('is_veg', '=', False)])
#     print("Non-Veg Foods:")
#     for f in foods:
#         print(f"Food: {f.name}, Price: {f.price}")

#     # 4. Update Food Price
#     food.write({'price': 350})
#     print(f"Updated Food Price: {food.price}")

#     # 5. Delete Food
#     food.unlink()
#     print("Food Deleted.")


# # You would run this script inside the Odoo environment
# if __name__ == "__main__":
#     from odoo import api, SUPERUSER_ID
#     env = api.Environment(SUPERUSER_ID, {})
#     orm_operations(env)
