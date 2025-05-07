# -*- coding: utf-8 -*-
# from odoo import http


# class ManufactureEmployeeCost(http.Controller):
#     @http.route('/manufacture_employee_cost/manufacture_employee_cost', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manufacture_employee_cost/manufacture_employee_cost/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('manufacture_employee_cost.listing', {
#             'root': '/manufacture_employee_cost/manufacture_employee_cost',
#             'objects': http.request.env['manufacture_employee_cost.manufacture_employee_cost'].search([]),
#         })

#     @http.route('/manufacture_employee_cost/manufacture_employee_cost/objects/<model("manufacture_employee_cost.manufacture_employee_cost"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manufacture_employee_cost.object', {
#             'object': obj
#         })

