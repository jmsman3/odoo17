# -*- coding: utf-8 -*-
# from odoo import http


# class BdcallingKpiSystem(http.Controller):
#     @http.route('/bdcalling_kpi_system/bdcalling_kpi_system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bdcalling_kpi_system/bdcalling_kpi_system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bdcalling_kpi_system.listing', {
#             'root': '/bdcalling_kpi_system/bdcalling_kpi_system',
#             'objects': http.request.env['bdcalling_kpi_system.bdcalling_kpi_system'].search([]),
#         })

#     @http.route('/bdcalling_kpi_system/bdcalling_kpi_system/objects/<model("bdcalling_kpi_system.bdcalling_kpi_system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bdcalling_kpi_system.object', {
#             'object': obj
#         })

