from odoo import models, fields, api

class Chef(models.Model):
    _name = 'foodpanda.chef'
    _description = 'Our Chef Profile'
    _inherit = ['mail.thread']
    
    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Profile Picture")
    speciality = fields.Char(string="Speciality Dish")
    experience_years = fields.Integer(string="Years of Experience")
    rating = fields.Float(string="Chef rating", digits=(2,1))
   

    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    active =  fields.Boolean(default=True)
    is_available = fields.Boolean(string="Currently Available")
    note = fields.Text(string="Additional Notes")

    food_order_id = fields.One2many("food.order", 'chef_id', string="Food orders") 


    @api.model
    def auto_mark_unavailable(self):
        chefs = self.search([('is_available', '=', True)])
        # for chef in chefs:
        #     chef.is_available = False
        #     print(f"Chef {chef.name} marked as unavailable ✅")
        # print(">>> Scheduler done: All available chefs are now unavailable.")

        chefs.write({'is_available': False})
        print(f"Scheduler done: {chefs} chefs markde as Unavailable.........>>>>!")








    def action_confirm(self):

#       #Direct sob search
        # chef_details = self.env['foodpanda.chef'].search([]) 
        # print("All chef er id number", chef_details)
        # for each_chef_taking in chef_details:
        #     print("Chef Name...", each_chef_taking.name)
        #     print("Chef Specialiti... ", each_chef_taking.speciality)
        #     print("Chef Experience... ", each_chef_taking.experience_years)
        #     print("Chef Rating... ", each_chef_taking.rating)

        #     print('\n')
 
        #     print(f"His name is {each_chef_taking.name} and is is Skilled in Cooking {each_chef_taking.speciality}. But he is {each_chef_taking.experience_years} years experience person. He has a Very Good rating that is {each_chef_taking.rating}")
        #     print('\n') 
      
# #------------------------------------------------------------------------------------------------------------
        specific_chef = self.env['foodpanda.chef'].search([('speciality', '=', 'Biscuit  Maker')])

        print("meat expert chef.....", specific_chef) 
        for i in specific_chef:
            print("Chef er name......", i.name)
            print("Chef er speciality ......", i.speciality)
            print("Chef er experience......", i.experience_years)
            print("Chef er rating......", i.rating)

        print('\n')

#         # phone_number_wise_search = self.env['foodpanda.chef'].search([('phone', '=','01753551489')])

#         # for p in phone_number_wise_search:
#         #     print("his name", i.name)
#         #     print("his speciality", i.speciality)
#         #     print("his experience" , p.experience_years)
#         #     print("his rating", p.rating)

            



#             # print("Sob Chef.........", chef_details)
#             # print("Chef Name...", rec.name)
#             # print("Chef Specialiti... ", chef_details.speciality)
#             # print("Chef Experience... ", chef_details.experience_years)
#             # print("Chef Rating... ", chef_details.rating)
      
    
#  #------------------------------------------------------------------------------------------------------------       
#         #conditional search here
#         chef_here = self.env['foodpanda.chef'].search([('speciality', '=', 'Fish')])
#         for result in chef_here:
#             print("the name...", result.name)
#             print("The speciality......", result.speciality)
#             print("His id...", result.id)
#             print('\n')
#             print("all fish-wala chef...",chef_here)
#             print('\n')
#  #------------------------------------------------------------------------------------------------------------       
#         #Operator (AND)-> testing
        # chef_and_operator = self.env['foodpanda.chef'].search([('experience_years', '>', '2'),('speciality', '=', 'Cholate  Maker')])
        # for chef_and in chef_and_operator:
        #     print("all the chefs....", chef_and)
        
# #------------------------------------------------------------------------------------------------------------      
#         #Operanto (Or)-> Testing 

#         chef_or_operator = self.env['foodpanda.chef'].search([('|'),('rating', '>', 4),('rating', '<',4)])
#         print("Based Chef OR Operator......", chef_or_operator)
#         print('\n')
#         for or_operatorr in chef_or_operator:
#             print("or name...", or_operatorr.name)
#             print("or rating.....", or_operatorr.rating)
#             print('\n')
#  #------------------------------------------------------------------------------------------------------------
#         #Search_Count
        # all_chef_detail = self.env['foodpanda.chef'].search([])
        # all_chef_detail_count = self.env['foodpanda.chef'].search_count([])
        # print("ALl chef Details...", all_chef_detail)
        # print("ALl chef COunt total...", all_chef_detail_count)
        # print('\n')
        
#         #Direct search 
#         chef_and_operator_count = self.env['foodpanda.chef'].search([('experience_years', '>', '2'),('speciality', '=', 'Fish')])

#         #Condition wise search count
#         chef_and_operator_cou Joy bangalant_now = self.env['foodpanda.chef'].search_count([('experience_years', '>', '2'),('speciality', '=', 'Fish')])
#         print("Experience and spciality wise count: ", chef_and_operator_count_now)
#  #------------------------------------------------------------------------------------------------------------


#        #Ref in Odoo
#         print('-------------------------Tree XML detail(id + name + model + xml soho)---------------------------------')
#         #for tree view --> format is - env.ref(Module name + Xml id name- Whether its Tree view and Form View Does not Matter)
#         chef_id_here = self.env.ref('foodpanda_management.view_chef_tree')
#         print("chef id is here......: ", chef_id_here.id)
#         print("View name here......: ", chef_id_here.name)
#         print("chef model here.......: ", chef_id_here.model)
#         print("chef xml er full arc.........", chef_id_here.arch)
#         print('\n')


#         #for form view->
#         print('-------------------------Form View XML detail(id + name + model + xml soho)---------------------------------')
#         chef_form_view_id_here = self.env.ref('foodpanda_management.view_chef_form')
#         print("form id........", chef_form_view_id_here.id)
#         print("form name........", chef_form_view_id_here.name)
#         print("form model name..........", chef_form_view_id_here.model)
#         print("for Architecture/Style xml structure.......", chef_form_view_id_here.arch)

#  #------------------------------------------------------------------------------------------------------------
#      #Browse here (Single object)
#         # browse_result = self.env['foodpanda.chef'].browse(1)
#         # print("My browsing result.....", browse_result)

#         # for chef_man in browse_result:
#         #     print("name...", chef_man.name)
#         #     print("Years of experience......", chef_man.experience_years)
#         #     print("His rating is......", chef_man.rating)  

#       #Browse Multiple Object but(Tuple use kora lagbe)
#         browse_multiple_chef = self.env['foodpanda.chef'].browse([1,2,3])
#         print("Multiple chef id.......", browse_multiple_chef)

#         for i in browse_multiple_chef:
#             print("---------------------------------------------------------------------------------------------------")
#             print(f"His id number is {i.id} and his name is {i.name} with Experience of {i.experience_years} Years.")
#             print("---------------------------------------------------------------------------------------------------")
#             print("Years of experience......", i.experience_years)
#             print("His rating is......", i.rating)
#             print('\n')  
# #------------------------------------------------------------------------------------------------------------------------------
#         check_exist_or_not = self.env['foodpanda.chef'].browse(5)
#         # search format is ---> (field_name, operator, value)
#         check_exist_or_not_by_search = self.env['foodpanda.chef'].search([('id', '=', '4' )])

#         if check_exist_or_not.exists():
#             print("Yesssssss Exist")
#         else:
#             print("Nooooooooooo data, Thank You")
        
#         print("\n")
#         # -------------------------------------------
#         if check_exist_or_not_by_search.exists():
#             print("Yesssssss Search Exist")
#         else:
#             print("Nooooooooooo Search data not exist, Thank You")
        
#         print("\n")
#         # .............................................
#         try:
#             check_exist = self.env['foodpanda.chef'].browse(544)
#             if check_exist.exists():
#                 print("Available ache")
#             else:
#                 print("Availabe nai")
#         except:
#             print("Kono data nai")
#         print('\n')
        
   #---------------------------------------------------------------------------------------------------------------------------
        # create Method 
        # vals = {
        #     'name': 'Joy bangala',
        #     'speciality': 'Apple juice  Maker',
        #     'experience_years': 1.1,
        #     'rating': 0.1

        # }
        # create_record = self.env['foodpanda.chef'].create(vals)
        # print("his name isss.....",create_record.name )
        # print("His speciality......",create_record.speciality )


        # print(f"New Record name is {create_record.name} With his Id Number -{create_record.id} \n His speciality is he is a {create_record.speciality} \n His is {create_record.experience_years} Years Experience person.\n Finally is ratig is {create_record.rating} \n")
    # ---------------------------------------------------------------------------------------------------------------------------
         #UPDATE an Existing Method.

        #  tep-1: aage dekhbo Browse deye Record ta Exist kore kina, Exists korle "Write"- Keyword deye Update kore debo
         
        # object_to_Update = self.env['foodpanda.chef'].search([('id' , '=' , '33')])
        # if object_to_Update.exists():
        #     val_update = {
        #         'speciality': 'Birthday Cake Makerrrrr',
        #         'email': 'neloyyy@gmail.com'
        #     }
        #     object_to_Update.write(val_update)
        # else:
        #     print("This id is not Exists,Please Try With Correct id,Thank You")
        

    #--------------------------------------------------------------------------------------------------------------------

       #Copy Method Here

        # information_to_copy = self.env['foodpanda.chef'].browse(33)
        # if information_to_copy.exists():
        #     information_to_copy.copy()
        #     print("Here....Done to Copy...", information_to_copy.name)
        # else:
        #     print("We are sorry broooooooo....")
    # #--------------------------------------------------------------------------------------------------------------------------------------------------

      
        # information_to_Delete_UNLINK = self.env['foodpanda.chef'].search([("id" , "=" , "26")])
        # information_to_Delete_UNLINK.unlink()
        # for t in information_to_Delete_UNLINK:
        #     print("name-----", t.name)

            
    




# ./odoo-bin -c ./debian/odoo.conf
#  /opt/odoo/odoo17/./odoo-bin --addons-path=/opt/odoo/odoo17/addons,/opt/odoo/odoo17/custom_addons, --xmlrpc-port=8069