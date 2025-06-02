# -*- coding: utf-8 -*-
# from odoo import http


# class BdcallingAccountingMod(http.Controller):
#     @http.route('/bdcalling_accounting_mod/bdcalling_accounting_mod', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bdcalling_accounting_mod/bdcalling_accounting_mod/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bdcalling_accounting_mod.listing', {
#             'root': '/bdcalling_accounting_mod/bdcalling_accounting_mod',
#             'objects': http.request.env['bdcalling_accounting_mod.bdcalling_accounting_mod'].search([]),
#         })

#     @http.route('/bdcalling_accounting_mod/bdcalling_accounting_mod/objects/<model("bdcalling_accounting_mod.bdcalling_accounting_mod"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bdcalling_accounting_mod.object', {
#             'object': obj
#         })

