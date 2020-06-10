# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import api
from odoo.exceptions import ValidationError


class SaleOrderAdds(models.Model):
    _inherit = 'sale.order'

    def default_costo_financiamiento(self):
        configuracion = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1)
        print('default configuracion',configuracion.name)
        if configuracion:
            return configuracion.costo_financiamiento
        else:
            return 0

    def action_delault_firma(self):
        return self.partner_id.signature

    @api.depends('x_porcentaje_utilidad')
    def _compute_porcentaje_utilidad(self):
        for record in self:
            record.x_porcentaje_utilidad_widget = record.x_porcentaje_utilidad * 100

    x_costo_financiamiento = fields.Float(
        string='Costo de financiamiento', default=default_costo_financiamiento)
    x_rendimiento = fields.Float(
        string='Rendimiento')
    x_comision = fields.Float(
        string='Comisión')
    x_equivalencia = fields.Float(
        string='Equivalencia')
    x_compra_asociada = fields.Many2one(
        'purchase.order', string='Orden de compra asociada')
    x_utilidad_bruta = fields.Float(string='Utilidad bruta')
    x_utilidad_venta = fields.Float(string='Utilidad de venta')
    x_porcentaje_utilidad = fields.Float(string='% Utilidad real')
    # este campo sólo se utiliza para mostar el valor en formato de porcentaje
    x_porcentaje_utilidad_widget = fields.Float(
        string='% Utilidad', compute='_compute_porcentaje_utilidad')
    x_utilidad_emdi = fields.Float(
        string='Utilidad EMDI')

    x_studio_firma_del_vendedor = fields.Binary()




    def action_confirm(self):
        configuracion_limite = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1).limite_confirmar_venta

        if self.amount_total >= configuracion_limite:
            if self.is_group_supervisor == False:
                raise ValidationError(
                    'El monto de la Orden requiere confirmación de Supervisor')
        return super(SaleOrderAdds, self).action_confirm()

    # @api.one
    def _compute_is_group_supervisor(self):
        self.ensure_one()
        self.is_group_supervisor = self.env['res.users'].has_group(
            'en_comisiones.group_supervisor_ventas')

    # Campo para revisar si el usuario actual es un administrador
    is_group_supervisor = fields.Boolean(
        string='Es supervisor',
        compute="_compute_is_group_supervisor",
    )


    @api.onchange('payment_term_id')
    def _onchange_payment_term_id(self):
        print(self.payment_term_id.name)
        if self.payment_term_id.name == 'Pago de contado':
            print("Ceros")
            self.x_costo_financiamiento = 0
            return
        else:
            print('tres')
            self.x_costo_financiamiento = 3
            return
        self.x_costo_financiamiento = 0
