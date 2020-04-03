# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockPickingMods(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('scheduled_date')
    def valida_grupo(self):
        if self.is_in_group == False:
            raise ValidationError(
                'Usuario actual no puede modificar Fecha Prevista')
        print(self.x_motivo_modificacion)
        if self.x_motivo_modificacion:
            print('razon seleccionada')
        else:
            raise ValidationError(
                'Para modificar campo de Fecha primero se debe seleccionar una Razón de cambio en fecha')

    #TODO: Esta validación se podría saltar si el usuario cambia fecha prevista y después borra la razón de cambio
    @api.onchange('x_motivo_modificacion') 
    def valida_grupo_motivo(self):
        if self.is_in_group == False:
            raise ValidationError(
                'Usuario actual no puede modificar Razón de cambio en fecha')

    @api.onchange('x_comentarios')
    def valida_grupo_comentarios(self):
        if self.is_in_group == False:
            raise ValidationError(
                'Usuario actual no puede modificar Comentarios')

    def _compute_is_group_mods(self):
        self.is_in_group = self.env['res.users'].has_group(
            'en_entregas.group_supervisor_movimientos')

    is_in_group = fields.Boolean(
        string='Puede modificar',
        compute="_compute_is_group_mods",
    )

    x_comentarios = fields.Text(
        string='Cometarios'
    )

    x_motivo_modificacion = fields.Many2one(
        'causa.cambio', string='Razón de cambio en fecha')
