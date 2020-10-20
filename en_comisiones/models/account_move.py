# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields
from odoo.exceptions import UserError

class FacturasComision(models.Model):
    _inherit = 'account.move'

    utilidad = fields.Monetary(String = 'Utilidad',digits = (10,2))
    margen_b = fields.Float(String="Margen",digits=(2,2))
    equivalencia = fields.Float(String="Equivalencia",digits=(2,2))
    rendimiento = fields.Monetary(String="Equivalencia",digits = (10,2))
    margen_real = fields.Float(String="Margen Real",digits=(2,2))
    equivalencia_u = fields.Float(String="Equivalencia",digits=(2,2))
    utilidad_ventas = fields.Monetary(String="Utilidad ventas",digits=(10,2))
    porcentaje_comision = fields.Float(String="Porcentaje comision",digits=(2,2))
    comision = fields.Monetary(String="Comision",digits=(10,2))
    costo_emdi = fields.Monetary(String="Cost EMDI",digits=(10,2))
    utilidad_emdi = fields.Monetary(String="Utilidad EMDI", digits=(10, 2))
    margen_emdi = fields.Float(String="Margen EMDI",digist=(2,2))
    costo_financiamiento = fields.Float(String="Costo de financiamiento",digits=(2,2))

    def button_draft(self):
        entregas = self.env['stock.picking'].search(
            [('state', '=', 'done'),
             ('efecto_counded_inv', '=', self.id)])

        for entrega in entregas:
            print(entrega.name,entrega.efecto_counded_inv)
            entrega.write({'efecto_counded_inv': 0})

        self.write({'utilidad':0,'margen_b':0,'equivalencia':0,'rendimiento':0,
                    'margen_real':0,'equivalencia_u':0,'utilidad_ventas':0,
                    'porcentaje_comision':0,'comision':0,'costo_emdi':0,
                    'utilidad_emdi':0,'margen_emdi':0,'costo_financiamiento':0})
        return super(FacturasComision, self).button_draft()


    def action_post(self):
        if self.type == 'out_invoice':
            self.calcularComision()
        return super(FacturasComision, self).action_post()

    def calcularComision(self):
        orden_venta = self.env['sale.order'].search(
             [('name', '=', self.invoice_origin)], limit=1)
        #Obtenemos todos las ordenes de compras generadas por la venta
        ordenes_de_compra = self.env['purchase.order'].search(
            [('origin', '=', orden_venta.name)])
        print(ordenes_de_compra.ids)
        #get all DS were state is done and is not counted
        subtotal_entregado = 0
        subtotal_venta = 0

        if ordenes_de_compra:
            for po_order in ordenes_de_compra:
                 entregas = self.env['stock.picking'].search(
                    [('origin', '=', po_order.name),
                     ('state','=','done'),
                     ('efecto_counded_inv','=',0)])
                 #
                 print(entregas.ids)
                 for entrega in entregas:
                     for linea_entrega in entrega.move_ids_without_package:
                        print(linea_entrega.quantity_done,linea_entrega.product_id.id)
                        price_purchase_product = (self.env['purchase.order.line'].search(
                         [('product_id', '=', linea_entrega.product_id.id),(
                             'order_id', '=',
                             po_order.name)]).mapped('price_unit'))
                        if len(price_purchase_product) > 0:
                            price_purchase_product = sum(price_purchase_product)/len(price_purchase_product)

                        subtotal_entregado += linea_entrega.quantity_done * price_purchase_product

                        price_product_sale = (self.env['sale.order.line'].search(
                            [('order_id', '=', orden_venta.name), (
                            'product_id', '=',
                            linea_entrega.product_id.id)]).mapped('price_unit'))
                        if len(price_product_sale) > 0:
                            price_product_sale = sum(price_product_sale)/len(price_product_sale)
                        subtotal_venta += linea_entrega.quantity_done * price_product_sale
                        print(subtotal_entregado,subtotal_venta)
                     entrega.update({'efecto_counded_inv':self.id})

            self.utilidad = subtotal_venta - subtotal_entregado
            self.margen_b = (self.utilidad / subtotal_entregado) * 100

            print(orden_venta.x_costo_financiamiento * 100, self.margen_b)
            self.costo_financiamiento = orden_venta.x_costo_financiamiento
            self.equivalencia = (self.costo_financiamiento * 100) / self.margen_b

            self.rendimiento = self.utilidad * (self.equivalencia / 100)

            self.margen_real = (self.margen_b - orden_venta.x_costo_financiamiento)

            self.equivalencia_u = ((self.margen_real * 100) / self.margen_b)

            self.utilidad_ventas = (self.utilidad * (self.equivalencia_u/100))
            self.porcentaje_comision = orden_venta.user_id.x_comision_ids[
                0].porcentaje
            self.comision = ((self.porcentaje_comision/100) * self.utilidad_ventas)
            print(' COMISION TIPO PAGO', orden_venta.x_costo_financiamiento)
            print(' subtotal entregado:', subtotal_entregado,
                  ' subtotal ventas:', round(subtotal_venta, 2),
                  ' utilidad:', self.utilidad)
            print(' margen:', self.margen_b, ' equivalencia:',
                  self.equivalencia, ' rendimeinto:',
                  self.rendimiento)
            print(' margen_real', self.margen_real, ' self.equivalencia',
                  self.equivalencia_u,
                  ' utilidad ventas', self.utilidad_ventas)
            print(' comision:', self.comision)
            print('saliendo de caluclo de comisiones :)')
            self.costo_emdi = self.comision + self.rendimiento + subtotal_entregado
            self.utilidad_emdi = subtotal_venta - self.costo_emdi
            self.margen_emdi = (1 - (self.costo_emdi/subtotal_venta)) * 100


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