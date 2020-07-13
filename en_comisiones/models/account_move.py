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

            #Obtenemos todos las ordenes de compras generadas por la venta
            ordenes_de_compra = self.env['purchase.order'].search(
                [('origin', '=', orden_venta.name)])
            compra_sub = 0

            #Toda Orden de compra debe tener un monto libre de impuesto > 0
            i = 0
            for purcharse_order in ordenes_de_compra:
                if purcharse_order.amount_untaxed < 0:
                    raise UserError(
                        'La Orden de Compra Asociada tiene Monto = 0')

                #Convertimos el subtotal de las ordenes de compra a pesos
                compra_sub += self._convert_precios_to_pesos(
                    purcharse_order.amount_untaxed,purcharse_order.currency_id)
                purcharse_order.write({'y_sale_order_id':orden_venta.id})
                if i == 0:
                    orden_venta.x_compra_asociada = purcharse_order.name
                    i += 1
                else:
                    orden_venta.x_compra_asociada += ','+purcharse_order.name


            #Convertimos el subtotal de ventas a pesos si no lo esta
            venta_sub = self._convert_precios_to_pesos\
                (orden_venta.amount_untaxed,orden_venta.pricelist_id.currency_id)

            print('Subtotal venta [E]', venta_sub)
            print('Subtotal compra [L]', compra_sub)
            utilidad_bruta = venta_sub - compra_sub
            print('Utilidad Bruta [I] = [E] - [L]', utilidad_bruta,venta_sub,compra_sub)
            porcentaje_utilidad = utilidad_bruta / compra_sub
            print('Porcentaje utilidad (Margen B) [J] = [I] / [L]', porcentaje_utilidad,utilidad_bruta,compra_sub)
            if porcentaje_utilidad <= 0:
                raise UserError(
                    'El porcentaje de utilidad debe ser mayor que  0')
            equivalencia = orden_venta.x_costo_financiamiento / porcentaje_utilidad
            print('Equivalencia [Q] = [P] / [J]', equivalencia,orden_venta.x_costo_financiamiento,porcentaje_utilidad)
            rendimiento = utilidad_bruta * (equivalencia / 100)
            print('Rendimiento [R] = [I] * [Q]', rendimiento,utilidad_bruta,(equivalencia / 100))
            margen_real = porcentaje_utilidad - (orden_venta.x_costo_financiamiento /100)
            print('Margen real [S] = [J] - [P]',margen_real,porcentaje_utilidad,(orden_venta.x_costo_financiamiento / 100))
            equivalencia_p = (margen_real / porcentaje_utilidad)
            print('Margen real [T] = (((S5*100)/J5/100))', margen_real, equivalencia_p, porcentaje_utilidad)
            utilidad_ventas = utilidad_bruta * rendimiento
            print('Utilidad Ventas [U] = [I] * [R]', utilidad_ventas,utilidad_bruta,rendimiento)
            utilidad_ventas_dos = utilidad_bruta * equivalencia_p
            print('Utilidad Ventas edit [U] = [I] * [T]', utilidad_ventas_dos, utilidad_bruta, equivalencia_p)
            porcentaje_comision = orden_venta.user_id.x_comision_ids[0].porcentaje
            print('Porcentaje comision [W]', porcentaje_comision)
            comision_venta_vendedor = utilidad_ventas_dos * \
                                      (porcentaje_comision / 100)
            print('comision Venta Vendedor [X] = [U] * [W]',
                  comision_venta_vendedor,utilidad_ventas_dos,
                  (porcentaje_comision / 100))
            orden_venta.x_rendimiento = rendimiento
            orden_venta.x_comision = comision_venta_vendedor
            costo_emdi = (comision_venta_vendedor + rendimiento + compra_sub)
            print('Costo emdi  = $Comision + Rendimiento + Subtotal compra',
                  costo_emdi, (comision_venta_vendedor +
                               rendimiento + compra_sub))
            orden_venta.x_equivalencia = equivalencia
            orden_venta.x_utilidad_bruta = utilidad_bruta
            orden_venta.x_utilidad_venta = utilidad_ventas_dos
            orden_venta.x_porcentaje_utilidad = porcentaje_utilidad
            orden_venta.x_utilidad_emdi = venta_sub - costo_emdi
            print('utilidad emdi',orden_venta.x_utilidad_emdi,venta_sub,costo_emdi)
        else:
            print('No, es inmediato:::::')
            orden_venta = self.env['sale.order'].search(
                [('name', '=', self.invoice_origin)])
            # Obtenemos todos las ordenes de compras generadas por la venta
            ordenes_de_compra = self.env['purchase.order'].search(
                [('origin', '=', orden_venta.name)])
            compra_sub = 0
            # Toda Orden de compra debe tener un monto libre de impuesto > 0
            i = 0
            for purcharse_order in ordenes_de_compra:
                if purcharse_order.amount_untaxed < 0:
                    raise UserError(
                        'La Orden de Compra Asociada tiene Monto = 0')

                # Convertimos el subtotal de las ordenes de compra a pesos
                compra_sub += self._convert_precios_to_pesos(
                    purcharse_order.amount_untaxed,
                    purcharse_order.currency_id)
                purcharse_order.write({'y_sale_order_id': orden_venta.id})
                if i == 0:
                    orden_venta.x_compra_asociada = purcharse_order.name
                    i += 1
                else:
                    orden_venta.x_compra_asociada += ','+purcharse_order.name

            # Convertimos el subtotal de ventas a pesos si no lo esta
            venta_sub = self._convert_precios_to_pesos \
                (orden_venta.amount_untaxed,
                 orden_venta.pricelist_id.currency_id)



            print('Subtotal venta [E]', venta_sub)
            print('Subtotal compra [L]', compra_sub)
            utilidad_bruta = venta_sub - compra_sub
            print('Utilidad Bruta [I] = [E] - [L]', utilidad_bruta, venta_sub,
                  compra_sub)
            porcentaje_utilidad = utilidad_bruta / compra_sub
            print('Porcentaje utilidad (Margen B) [J] = [I] / [L]',
                  porcentaje_utilidad, utilidad_bruta, compra_sub)
            if porcentaje_utilidad <= 0:
                raise UserError(
                    'El porcentaje de utilidad debe ser mayor que  0')
            equivalencia = orden_venta.x_costo_financiamiento / porcentaje_utilidad
            print('Equivalencia [Q] = [P] / [J]', equivalencia,
                  orden_venta.x_costo_financiamiento, porcentaje_utilidad)
            rendimiento = utilidad_bruta * (equivalencia / 100)
            print('Rendimiento [R] = [I] * [Q]', rendimiento, utilidad_bruta,
                  (equivalencia / 100))
            margen_real = porcentaje_utilidad - (
                        orden_venta.x_costo_financiamiento / 100)
            print('Margen real [S] = [J] - [P]', margen_real,
                  porcentaje_utilidad,
                  (orden_venta.x_costo_financiamiento / 100))
            equivalencia_p = (margen_real / porcentaje_utilidad)
            print('Margen real [T] = (((S5*100)/J5/100))', margen_real,
                  equivalencia_p, porcentaje_utilidad)
            utilidad_ventas = utilidad_bruta * rendimiento
            print('Utilidad Ventas [U] = [I] * [R]', utilidad_ventas,
                  utilidad_bruta, rendimiento)
            utilidad_ventas_dos = utilidad_bruta * equivalencia_p
            print('Utilidad Ventas edit [U] = [I] * [T]', utilidad_ventas_dos,
                  utilidad_bruta, equivalencia_p)
            porcentaje_comision = orden_venta.user_id.x_comision_ids[
                0].porcentaje
            print('Porcentaje comision [W]', porcentaje_comision)
            comision_venta_vendedor = utilidad_ventas_dos * \
                                      (porcentaje_comision / 100)
            print('comision Venta Vendedor [X] = [U] * [W]',
                  comision_venta_vendedor, utilidad_ventas_dos,
                  (porcentaje_comision / 100))
            orden_venta.x_rendimiento = rendimiento
            orden_venta.x_comision = comision_venta_vendedor
            costo_emdi = (comision_venta_vendedor + rendimiento + compra_sub)
            print('Costo emdi  = $Comision + Rendimiento + Subtotal compra',
                  costo_emdi, ( comision_venta_vendedor +
                                rendimiento + compra_sub))
            orden_venta.x_equivalencia = equivalencia
            orden_venta.x_utilidad_bruta = utilidad_bruta
            orden_venta.x_utilidad_venta = utilidad_ventas_dos
            orden_venta.x_porcentaje_utilidad = porcentaje_utilidad
            orden_venta.x_utilidad_emdi = venta_sub - costo_emdi
            print('utilidad emdi', orden_venta.x_utilidad_emdi,venta_sub,costo_emdi)


            # costo = orden_venta.amount_untaxed
            # print('costo', costo)
            # utilidad_bruta = costo - orden_compra.amount_untaxed
            # print('Utilidad Bruta', utilidad_bruta)
            # porcentaje_comision = orden_venta.user_id.x_comision_ids[0].porcentaje
            # print('Porcentaje comision', porcentaje_comision)
            # comision_venta_vendedor = utilidad_bruta * \
            #     (porcentaje_comision / 100)
            # print('comision Venta Vendedor', comision_venta_vendedor)
            # porcentaje_utilidad = utilidad_bruta / orden_compra.amount_untaxed
            # print('Porcentaje utilidad', porcentaje_utilidad)
            # if porcentaje_utilidad <= 0:
            #     raise UserError(
            #         'El porcentaje de utilidad debe ser mayor que  0')
            # equivalencia = orden_venta.x_costo_financiamiento / porcentaje_utilidad
            # print('Equivalencia', equivalencia)
            # rendimiento = utilidad_bruta * (equivalencia / 100)
            # print('Rendimiento', rendimiento)
            # orden_venta.x_equivalencia = equivalencia
            # orden_venta.x_rendimiento = rendimiento
            # orden_venta.x_utilidad_bruta = utilidad_bruta
            # orden_venta.x_compra_asociada = orden_compra.id
            # orden_venta.x_comision = comision_venta_vendedor
            # orden_venta.x_porcentaje_utilidad = porcentaje_utilidad
            # orden_venta.x_utilidad_emdi = costo - (comision_venta_vendedor + \
            #                               rendimiento + \
            #                               orden_compra.amount_untaxed)
                # utilidad_bruta - rendimiento - \
                # comision_venta_vendedor

            # utilidad_ventas = utilidad_bruta * rendimiento
            # print('Utilidad Ventas', utilidad_ventas)
            #
            # orden_venta.x_utilidad_venta = utilidad_ventas
        
        # if True:
        #    raise UserError('stop:::::')


    #Convetir a pesos dependiendo la moneda
    def _convert_precios_to_pesos(self, monto , currency_id=False):
        #print('************Convertiendo*************')
        #print(product_id.name,pricelist)

        if currency_id.name != 'MXN':
            mon = self.env['res.currency'].search(
                [('name', '=',currency_id.name)],
                limit=1)
            return monto / (mon.rate * 1)

        return monto

    def _igualar_moneda(self,monto , pricelist_venta=False,moneda=False):
        #print('************Convertiendo*************')

        if pricelist_venta and moneda :
            moneda_venta = self.env['product.pricelist'].search(
                [('id', '=', pricelist_venta.id)], limit=1)

            print('Monto', monto, 'Moneda de la venta',moneda_venta.name,'Moneda compra',moneda.name)


            if moneda_venta.currency_id.name != moneda.name :
                print('Las monedas son diferentes')
                print('venta y compra diferentes monedas',moneda_venta.currency_id.name,moneda.name)
                usd = self.env['res.currency'].search(
                    [('name', '=', 'USD')],
                    limit=1)

                if moneda_venta.currency_id.name == 'USD' and moneda.name == 'MXN':
                    print('Moneda de venta USD y moneda de compra es MXN')
                    print('monto compra a pesos',monto * usd.rate,monto,usd.rate )

                    return monto * usd.rate

                if moneda_venta.currency_id.name == 'MXN' and moneda.name == 'USD':

                    print('monto compra a dolares', monto / (usd.rate * 1) ,monto,usd.rate )
                    return monto / (usd.rate * 1)

        return monto