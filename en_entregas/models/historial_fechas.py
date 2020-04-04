# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HistorialFechas(models.Model):
    _name = 'historial.fechas'
    _description = 'Histórico de modificaciones en el campo de fecha prevista de Movimientos Albarán'

    name = fields.Many2one('res.users', string='Usuario', required=True)
    fecha_anterior = fields.Datetime(string='Fecha anterior')
    fecha_actualizada = fields.Datetime(string='Fecha actualizada')
    motivo_modificacion = fields.Many2one(
        'causa.cambio', string='Razón de cambio en fecha')
    comentarios = fields.Text(string='Comentarios')
    picking_id = fields.Many2one(
        'stock.picking',
        string="Movimiento",
        copy=False
    )
