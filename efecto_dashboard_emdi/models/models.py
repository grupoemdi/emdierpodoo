#-*- coding: utf-8 -*-

from odoo import models, fields, api


class efecto_dashboard_emdi(models.Model):
    _name = 'comisiones.dashboard'
    _description = 'Clase para manejar los elementos en el dashboard'

    name = fields.Char()
    uerers = fields.Char(string="Vendedor",readonly="True")
