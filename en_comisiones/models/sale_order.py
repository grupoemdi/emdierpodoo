# -*- coding: utf-8 -*-

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class SaleOrderAdds(models.Model):
    _inherit = 'sale.order'



    def action_delault_firma(self):
        return self.partner_id.signature

    @api.depends('x_porcentaje_utilidad')
    def _compute_porcentaje_utilidad(self):
        for record in self:
            record.x_porcentaje_utilidad_widget = record.x_porcentaje_utilidad * 100



    x_costo_financiamiento = fields.Float(
        string='Costo de financiamiento')
    x_rendimiento = fields.Float(
        string='Rendimiento')
    x_comision = fields.Float(
        string='Comisión')
    x_equivalencia = fields.Float(
        string='Equivalencia')
    x_compra_asociada = fields.Text(string="Ordenes de compra asociadas")
    y_purchase_order_ids = fields.One2many('purchase.order',
                                         'y_sale_order_id')
    x_utilidad_bruta = fields.Float(string='Utilidad bruta')
    x_utilidad_venta = fields.Float(string='Utilidad de venta')
    x_porcentaje_utilidad = fields.Float(string='% Utilidad real')
    # este campo sólo se utiliza para mostar el valor en formato de porcentaje
    x_porcentaje_utilidad_widget = fields.Float(
        string='% Utilidad', compute='_compute_porcentaje_utilidad')
    x_utilidad_emdi = fields.Float(
        string='Utilidad EMDI')

    #x_studio_firma_del_vendedor = fields.Binary()




    def action_confirm(self):
        configuracion_limite = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1).limite_confirmar_venta

        if self.amount_total >= configuracion_limite:
            if self.is_group_supervisor == False:
                raise ValidationError(
                    'El monto de la Orden requiere confirmación de Supervisor')
        return super(SaleOrderAdds, self).action_confirm()

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
        #Search de first element
        payment_term = self.env['account.payment.term'].search(
            [], limit=1)
        print(self.payment_term_id.id,'cambio')
        if self.payment_term_id.id == payment_term.id:
            self.x_costo_financiamiento = 0
            return
        if self.payment_term_id.id != False:
            self.x_costo_financiamiento = 3
            return
        self.x_costo_financiamiento = 0

    def _action_confirm(self):
        """ Generate inter company purchase order based on conditions """
        res = super(SaleOrderAdds, self)._action_confirm()
        ordenes_de_compra = self.env['purchase.order'].search(
            [('origin', '=', self.name)])
        i = 0
        for purcharse_order in ordenes_de_compra:
            purcharse_order.write({'y_sale_order_id': self.id})
            if i == 0:
                self.x_compra_asociada = purcharse_order.name
                i += 1
            else:
                self.x_compra_asociada += ','+purcharse_order.name
        return res

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        orden_venta = super(SaleOrderAdds, self).copy(default=default)
        orden_venta.x_rendimiento = 0
        orden_venta.x_comision = 0
        orden_venta.x_equivalencia = 0
        orden_venta.x_utilidad_bruta = 0
        orden_venta.x_utilidad_venta = 0
        orden_venta.x_porcentaje_utilidad = 0
        orden_venta.x_utilidad_emdi = 0
        orden_venta.x_compra_asociada = ""
        return orden_venta


class purchaseOrderComisiones(models.Model):
    _inherit = 'purchase.order'

    y_sale_order_id = fields.Many2one(
        'sale.order', string='Orden de venta asociada')


