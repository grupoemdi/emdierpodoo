# -*- coding: utf-8 -*-

#from odoo import fields
import calendar
from datetime import date
from datetime import datetime
from odoo import api
from odoo import models
#from odoo.exceptions import UserError


class FacturasRecargo(models.Model):
    _name = "ordenes.comisiones"
    _description = 'Generar ordenes de compra para comisiones'

    @api.model
    def ordenes_venta_comisiones(self):
        print("Ejecutando accion planificada Creando Ordenes")
        #fecha_actual = datetime.now().date().year
        #fecha_actual = date.today()
        configuracion = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1)
        if configuracion.producto_pago_comision:
            producto_comision = configuracion.producto_pago_comision
            producto_rendimiento = configuracion.producto_pago_servicio
        else:
            print("Falta configuracion")
            # raise UserError(
            # 'Pago: No hay configuración de producto pago configuración en Ventas->Configuración->Comisiones')

        anio = datetime.now().date().year
        mes = datetime.now().date().month
        dia_primero = date(anio, mes, 1)
        usuario_ids = self.env['res.users'].search(
            [('id', '>', 0)])
        for usuario in usuario_ids:
            comision_mes_ids = self.env['comisiones.pagos'].search(
                [('fecha', '>', dia_primero), ('fecha', '<=', date.today()), ('name.user_id.id', '=', usuario.id), ('procesado', '=', False)])
            print("Creando SO::::: USUARIO ", usuario.name)
            if comision_mes_ids:
                orden_values = {
                    'partner_id': configuracion.partner_proveedor_po.id,
                    #'partner_id': usuario.commercial_partner_id.id,
                    'partner_ref': usuario.name,
                    'date_order': datetime.now(),
                    #'create_uid': usuario.id,
                    'user_id': usuario.id,
                }
                orden_creada = self.env['purchase.order'].create(orden_values)
                rendimiento_pago = 0
                for record in comision_mes_ids:
                    print("Creando Lineas::::")
                    linea_data = {
                        'order_id': orden_creada.id,
                        'product_id': producto_comision.id,
                        'name': 'Pago de comisión del '+str(record.fecha.day) + self.busca_mes(record.fecha.month) + ' de ' + str(record.fecha.year) + " / " + str(record.name.name),
                        'product_qty': 1,
                        'price_unit': record.comision_pago,
                        'product_uom': producto_comision.uom_id.id,
                        'date_planned': datetime.now(),
                        'taxes_id': producto_comision.taxes_id,
                    }
                    linea_crear = self.env['purchase.order.line'].create(
                        linea_data)
                    record.procesado = True
                    rendimiento_pago += record.rendimiento_pago
                linea_comision_data = {
                    'order_id': orden_creada.id,
                    'product_id': producto_rendimiento.id,
                    'name': 'Pago de rendimiento',
                    'product_qty': 1,
                    'price_unit': rendimiento_pago,
                    'product_uom': producto_rendimiento.uom_id.id,
                    'date_planned': datetime.now(),
                    'taxes_id': producto_rendimiento.taxes_id,
                }
                linea_crear = self.env['purchase.order.line'].create(
                    linea_comision_data)
                #orden_creada.write({'partner_id': 3})
                #print('ULTIMA::', orden_creada.partner_id.name)
        print('Fin accion planificada')

    def busca_mes(self, mes):  # TODO mejorar esta función
        if mes == 1:
            return " de enero"
        elif mes == 2:
            return "  de febrero"
        elif mes == 3:
            return "  de marzo"
        elif mes == 4:
            return "  de abril"
        elif mes == 5:
            return "  de mayo"
        elif mes == 6:
            return "  de junio"
        elif mes == 7:
            return "  de julio"
        elif mes == 8:
            return "  de agosto"
        elif mes == 9:
            return "  de septiembre"
        elif mes == 10:
            return "  de octubre"
        elif mes == 11:
            return "  de noviembre"
        elif mes == 12:
            return "  de diciembre"
        else:
            return ""
