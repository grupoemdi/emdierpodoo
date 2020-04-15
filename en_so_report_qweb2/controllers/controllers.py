# -*- coding: utf-8 -*-
# from odoo import http


# class Addons\extra-addons\prueba(http.Controller):
#     @http.route('/addons\extra-addons\prueba/addons\extra-addons\prueba/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/addons\extra-addons\prueba/addons\extra-addons\prueba/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('addons\extra-addons\prueba.listing', {
#             'root': '/addons\extra-addons\prueba/addons\extra-addons\prueba',
#             'objects': http.request.env['addons\extra-addons\prueba.addons\extra-addons\prueba'].search([]),
#         })

#     @http.route('/addons\extra-addons\prueba/addons\extra-addons\prueba/objects/<model("addons\extra-addons\prueba.addons\extra-addons\prueba"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('addons\extra-addons\prueba.object', {
#             'object': obj
#         })
