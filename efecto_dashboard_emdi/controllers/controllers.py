# -*- coding: utf-8 -*-
# from odoo import http


# class EfectoDashboardEmdi(http.Controller):
#     @http.route('/efecto_dashboard_emdi/efecto_dashboard_emdi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/efecto_dashboard_emdi/efecto_dashboard_emdi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('efecto_dashboard_emdi.listing', {
#             'root': '/efecto_dashboard_emdi/efecto_dashboard_emdi',
#             'objects': http.request.env['efecto_dashboard_emdi.efecto_dashboard_emdi'].search([]),
#         })

#     @http.route('/efecto_dashboard_emdi/efecto_dashboard_emdi/objects/<model("efecto_dashboard_emdi.efecto_dashboard_emdi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('efecto_dashboard_emdi.object', {
#             'object': obj
#         })
