# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CausaCambio(models.Model):
    _name = 'causa.cambio'
    _description = 'Motivos por los cuales se realiza cambio de fecha'

    name = fields.Char(string='Razón de cambio en fecha', required=True)
    