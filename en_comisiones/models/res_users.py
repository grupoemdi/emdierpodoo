# -*- coding: utf-8 -*-
import calendar
from datetime import date
from datetime import datetime
from odoo import models, fields, api


class PUsersComisiones(models.Model):
    _inherit = 'res.users'

    x_venta_minimo_mensual = fields.Float(
        string='Monto de Venta mínimo mensual')

    x_venta_mes = fields.Float(
        string='Monto vendido (Mes en curso)')

    x_objetivo_mensual = fields.Float(
        string='Objetivo de Venta (mensual)')

    x_porcentaje_comisión = fields.Float(
        string='Porcentaje de Comisión')

    x_comision_ids = fields.One2many(
        'porcentaje.comision',
        'user_id',
        string="Comisiones"
    )

    x_producto_id = fields.Many2one(
        'product.product', string='Producto asociado')

    x_cc = fields.Selection(
        [('imss', 'IMSS'), ('freelance', 'Freelance')], 'CC')

    x_salario = fields.Float(string='Salario')

    x_bonos = fields.Float(string='Bonos')

    x_deducciones = fields.Float(string='Deducciones')

    x_imss_obrera = fields.Float(string='IMSS (aprotación obrera)')

    x_isr = fields.Float(string='ISR (aportación obrera)')

    x_imss_patronal = fields.Float(string='IMSS (aportación patronal)')

    x_infonavit = fields.Float(string='INFONAVIT (aportación patronal)')

    def _get_comisiones_rendimiento(self):
        print("USUARIO::",self.name)
        rendimiento_comision = []
        comisiones_pagos = []
        anio = datetime.now().date().year
        mes = datetime.now().date().month
        dia_primero = date(anio, mes, 1)
        comision_mes_ids = self.env['comisiones.pagos'].search(
            [('fecha', '>', dia_primero), ('fecha', '<=', date.today()), ('name.user_id.id', '=', self.id), ('procesado', '=', False)])
        comisiones_total = 0
        rendimiento_total = 0
        # comisiones_total = sum(
        #     line.comision_pago for line in self.comision_mes_ids)
        # rendimiento_total = sum(
        #     line.rendimiento_pago for line in self.comision_mes_ids)
        for comision in comision_mes_ids:
            comisiones_total += comision.comision_pago
            rendimiento_total += comision.rendimiento_pago
            comisiones_pagos.append(comision.id)
            comision.procesado= True
        rendimiento_comision.extend([comisiones_total, rendimiento_total])
        rendimiento_comision.append(comisiones_pagos)
        
        return rendimiento_comision


class PorcentajeComision(models.Model):
    _name = 'porcentaje.comision'
    _description = 'Porcentaje de comisión para el usuario'

    minimo = fields.Float(
        string='Mínimo')

    maximo = fields.Float(
        string='Máximo')

    porcentaje = fields.Float(
        string='Porcentaje')

    user_id = fields.Many2one(
        'res.users',
        string='usuario')
