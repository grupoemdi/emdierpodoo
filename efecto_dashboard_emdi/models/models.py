#-*- coding: utf-8 -*-

from odoo import models, fields, api


class efecto_dashboard_emdi(models.Model):
    _name = 'comisiones.dashboard'
    _description = 'Clase para manejar los elementos en el dashboard'

    name = fields.Char(string="nombre")
    uerers = fields.Char(string="Vendedor",readonly="True")


class sale_order_dashboard(models.Model):
    _name = "sale.dashboard"


    name = fields.Char(String="Custom char")
    another_field = fields.Char(string="nombre")


class sale_order_inherit(models.Model):
    _inherit = "sale.order"

    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)


    def _get_attendees_count(self):
        return 1;




