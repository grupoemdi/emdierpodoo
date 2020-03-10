# -*- coding: utf-8 -*-

from odoo import models, fields


class ConfiguracionComisiones(models.Model):
    _name = "configuracion.comisiones"
    _description = "Configuración para comisiones"

    name = fields.Char('Nombre configuración', required=True)

    costo_financiamiento = fields.Float(
        string='Costo de financiamiento')

    metodo_pago_inmediato = fields.Many2one(
        'account.payment.term', string='Método de pago inmediato')

    producto_pago_comision = fields.Many2one(
        'product.product', string='Producto que es pago de comisión')
    producto_inversion = fields.Many2one(
        'product.product', string='Producto que es inversión')
    producto_pago_servicio = fields.Many2one(
        'product.product', string='Producto para pago de servicio')
    limite_confirmar_venta = fields.Float(
        string='Monto máximo para confirmar orden por Comercial')
    partner_proveedor_po = fields.Many2one(
        'res.partner', string='Proveedor en PO')
    partner_proveedor_po = fields.Many2one(
        'res.partner', string='Proveedor en PO')
    
    porcentaje_comision_out = fields.Float(string = 'Porcentaje Comisión')
    # def getComision(self):
    #     configuracion = self.env['configuracion.comisiones'].search(
    #         [('id', '!=', 0)], limit=1)
    #     if configuracion:
    #         return configuracion.costo_financiamiento
    #     else:
    #         return 0
    #     return folio
