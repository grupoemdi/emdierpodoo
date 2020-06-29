# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError


class FacturasComision(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        if self.type == 'out_invoice':
            self.calcularComision()
        return super(FacturasComision, self).action_post()

    def calcularComision(self):
        configuracion = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1)
        if configuracion.metodo_pago_inmediato:
            metodo_inmediato = configuracion.metodo_pago_inmediato
        else:
            raise UserError(
                'No hay configuración de pago inmediato en Ventas->Configuración->Comisiones')


        print(self.invoice_payment_term_id.id,metodo_inmediato.id)
        if self.invoice_payment_term_id.id != metodo_inmediato.id:
            orden_venta = self.env['sale.order'].search(
                [('name', '=', self.invoice_origin)], limit=1)
            orden_compra = self.env['purchase.order'].search(
                [('origin', '=', orden_venta.name)], limit=1)
            if orden_compra.amount_untaxed == 0:
                raise UserError(
                'La Orden de Compra Asociada tiene Monto = 0')
            print('orden compra:', orden_compra.name)

            costo = orden_venta.amount_untaxed
            print('costo', costo)

            utilidad_bruta = costo - orden_compra.amount_untaxed
            print('Utilidad Bruta', utilidad_bruta)

            porcentaje_utilidad = utilidad_bruta / orden_compra.amount_untaxed
            print('Porcentaje utilidad', porcentaje_utilidad)

            if porcentaje_utilidad <= 0:
                raise UserError(
                    'El porcentaje de utilidad debe ser mayor que  0')
            equivalencia = orden_venta.x_costo_financiamiento / porcentaje_utilidad
            print('Equivalencia', equivalencia)

            rendimiento = utilidad_bruta * (equivalencia / 100)
            print('Rendimiento', rendimiento)

            utilidad_ventas = utilidad_bruta * rendimiento
            print('Utilidad Ventas', utilidad_ventas)

            porcentaje_comision = orden_venta.user_id.x_comision_ids[0].porcentaje
            print('Porcentaje comision', porcentaje_comision)

            comision_venta_vendedor = utilidad_ventas * \
                (porcentaje_comision / 100)
            print('comision Venta Vendedor', comision_venta_vendedor)

            orden_venta.x_rendimiento = rendimiento
            orden_venta.x_comision = comision_venta_vendedor
            orden_venta.x_equivalencia = equivalencia
            orden_venta.x_compra_asociada = orden_compra.id
            orden_venta.x_utilidad_bruta = utilidad_bruta
            orden_venta.x_utilidad_venta = utilidad_ventas
            orden_venta.x_porcentaje_utilidad = porcentaje_utilidad
            orden_venta.x_utilidad_emdi = costo - (comision_venta_vendedor + \
                                          rendimiento + \
                                          orden_compra.amount_untaxed)
        else:
            print('No, es inmediato:::::')
            orden_venta = self.env['sale.order'].search(
                [('name', '=', self.invoice_origin)], limit=1)
            orden_compra = self.env['purchase.order'].search(
                [('origin', '=', orden_venta.name)], limit=1)
            if orden_compra.amount_untaxed == 0:
                raise UserError(
                'La Orden de Compra Asociada tiene Monto = 0')
            costo = orden_venta.amount_untaxed
            print('costo', costo)
            utilidad_bruta = costo - orden_compra.amount_untaxed
            print('Utilidad Bruta', utilidad_bruta)
            porcentaje_comision = orden_venta.user_id.x_comision_ids[0].porcentaje
            print('Porcentaje comision', porcentaje_comision)
            comision_venta_vendedor = utilidad_bruta * \
                (porcentaje_comision / 100)
            print('comision Venta Vendedor', comision_venta_vendedor)
            porcentaje_utilidad = utilidad_bruta / orden_compra.amount_untaxed
            print('Porcentaje utilidad', porcentaje_utilidad)
            if porcentaje_utilidad <= 0:
                raise UserError(
                    'El porcentaje de utilidad debe ser mayor que  0')
            equivalencia = orden_venta.x_costo_financiamiento / porcentaje_utilidad
            print('Equivalencia', equivalencia)
            rendimiento = utilidad_bruta * (equivalencia / 100)
            print('Rendimiento', rendimiento)
            orden_venta.x_equivalencia = equivalencia
            orden_venta.x_rendimiento = rendimiento
            orden_venta.x_utilidad_bruta = utilidad_bruta
            orden_venta.x_compra_asociada = orden_compra.id
            orden_venta.x_comision = comision_venta_vendedor
            orden_venta.x_porcentaje_utilidad = porcentaje_utilidad
            orden_venta.x_utilidad_emdi = costo - (comision_venta_vendedor + \
                                          rendimiento + \
                                          orden_compra.amount_untaxed)
                # utilidad_bruta - rendimiento - \
                # comision_venta_vendedor

            utilidad_ventas = utilidad_bruta * rendimiento
            print('Utilidad Ventas', utilidad_ventas)

            orden_venta.x_utilidad_venta = utilidad_ventas
        
        # if True:
        #    raise UserError('stop:::::')
