# -*- coding: utf-8 -*-
# from odoo import http


# class BdPurchaseRequisition(http.Controller):
#     @http.route('/bd_purchase_requisition/bd_purchase_requisition', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bd_purchase_requisition/bd_purchase_requisition/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bd_purchase_requisition.listing', {
#             'root': '/bd_purchase_requisition/bd_purchase_requisition',
#             'objects': http.request.env['bd_purchase_requisition.bd_purchase_requisition'].search([]),
#         })

#     @http.route('/bd_purchase_requisition/bd_purchase_requisition/objects/<model("bd_purchase_requisition.bd_purchase_requisition"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bd_purchase_requisition.object', {
#             'object': obj
#         })

