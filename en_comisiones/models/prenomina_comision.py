# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError


class PrenominaComision(models.Model):
    _name = "prenomina.comision"
    _description = "Prenomina Ejecución"

    name = fields.Char('Nombre de Prenomina', required=True)

    fecha = fields.Datetime('Fecha (automática)')

    purchase_order_id = fields.Many2one('purchase.order', string='PO Asociada')

    prenomina_line = fields.One2many(comodel_name='prenomina.comision.line',
                                     inverse_name='prenomina_id',
                                     string="Líneas de prenomina")

    state = fields.Selection(
        [('borrador', 'borrador'), ('populated', 'Populated'), ('confirmada', 'confirmada')], 'Estado',  default='borrador')

    # CAMPOS PARA TOTALES
    subtotal_ingreso = fields.Float(
        string='Subtotal Ingreso', compute='_compute_subtotal_ingreso',)

    comision_nomina = fields.Float(
        string='Comisión Nómina', compute='_compute_comision_nomina')

    impuestos_aportacion_obrera = fields.Float(
        string='Impuestos Aportación Obrera', compute='_compute_aportacion_obrera')

    ingreso_neto_dispersion = fields.Float(
        string='Ingreso Neto (Dispersión)', compute='_compute_ingreso_neto')

    impuestos_aportacion_patronal = fields.Float(
        string='Impuestos Aportación Patronal', compute='_compute_aportacion_patronal')

    total_deposito_nomina = fields.Float(
        string='Total Depósito Nómina', compute='_compute_total_deposito_nomina')

    flujo_efectivo_deposito = fields.Float(string='Flujo de Efectivo Deposito')

    total_totales = fields.Float(
        string='Total', compute='_compute_total_totales')

    # CAMPOS OC
    subtotal_co = fields.Float(
        string='Subtotal', compute='_compute_subtotal_co')

    iva_oc = fields.Float(string='IVA', compute='_compute_iva_oc')

    @api.model
    def create(self, vals):
        prenomina_creada = super(PrenominaComision, self).create(vals)
        print('Marcar como procesados los pagos-comisiones:::')
        # for record in self.prenomina_line: #Marcar como procesados los pagos-comisiones
        #    for line in record.comision_pago_line:
        #        line.procesado = True
        return prenomina_creada

    def get_data_comision(self):
        print("Obteniendo datos")
        # configuracion = self.env['configuracion.comisiones'].search(
        #     [('id', '!=', 0)], limit=1)
        # if configuracion.producto_pago_comision:
        #     producto_comision = configuracion.producto_pago_comision
        #     producto_rendimiento = configuracion.producto_pago_servicio
        # else:
        #     raise UserError(
        #         'No hay configuración de producto pago configuración en Ventas->Configuración->Comisiones')
        for record in self.prenomina_line:
            record.unlink()
        usuario_ids = self.env['res.users'].search(
            [('id', '>', 0)])
        for usuario in usuario_ids:
            data_comision_rendimiento = usuario._get_comisiones_rendimiento()
            linea_prenomina_data = {
                'cc_info': usuario.x_cc,
                'name': usuario.id,
                'salario': usuario.x_salario,
                'comisiones': data_comision_rendimiento[0],
                'rendimiento': data_comision_rendimiento[1],
                'imss_obrera': usuario.x_imss_obrera,
                'isr': usuario.x_isr,
                'imss_patronal': usuario.x_imss_patronal,
                'infonavit': usuario.x_infonavit,
                'prenomina_id': self.id,
                'comision_pago_line': [(6, 0, data_comision_rendimiento[2])]
            }
            linea_prenomina_creada = self.env['prenomina.comision.line'].create(
                linea_prenomina_data)
            self.state = 'populated'
            # CHIDO
            #data_comision_rendimiento = usuario._get_comisiones_rendimiento()
            # linea_prenomina_creada.comisiones = data_comision_rendimiento[0]
            # linea_prenomina_creada.rendimiento = data_comision_rendimiento[1]
            # linea_prenomina_creada.comision_pago_line = [
            #     (6, 0, data_comision_rendimiento[2])]

    def create_so_comision(self):
        print("Generando SO")
        configuracion = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1)
        if configuracion.partner_proveedor_po:
            print('Configuration load')
        else:
            raise UserError(
                'Pago: No hay configuración de Partner en SO Ventas->Configuración->Comisiones')
        orden_values = {
            'partner_id': configuracion.partner_proveedor_po.id,
            # 'partner_id': usuario.commercial_partner_id.id,
            # 'partner_ref': usuario.name,
            'date_order': datetime.now(),
            # 'create_uid': usuario.id,
            # 'user_id': usuario.id,
        }
        orden_creada = self.env['purchase.order'].create(orden_values)
        for record in self.prenomina_line:
            linea_data = {
                'order_id': orden_creada.id,
                'product_id': record.name.x_producto_id.id,
                'name': record.name.x_producto_id.name,
                'product_qty': 1,
                'price_unit': record.ingreso_neto,
                'product_uom': record.name.x_producto_id.uom_id.id,
                'date_planned': datetime.now(),
                'taxes_id': record.name.x_producto_id.taxes_id,
            }
            linea_crear = self.env['purchase.order.line'].create(
                linea_data)
        self.purchase_order_id = orden_creada.id
        self.state = 'confirmada'

    @api.depends('prenomina_line.subtotal')
    def _compute_subtotal_ingreso(self):
        self.subtotal_ingreso = sum(
            line.subtotal for line in self.prenomina_line)

    @api.depends('prenomina_line.comision_diez')
    def _compute_comision_nomina(self):
        self.comision_nomina = sum(
            line.comision_diez for line in self.prenomina_line)

    @api.depends('prenomina_line.imss_obrera', 'prenomina_line.isr')
    def _compute_aportacion_obrera(self):
        total_imss = sum(
            line.imss_obrera for line in self.prenomina_line)
        total_isr = sum(
            line.isr for line in self.prenomina_line)
        self.impuestos_aportacion_obrera = total_imss + total_isr

    @api.depends('prenomina_line.ingreso_neto')
    def _compute_ingreso_neto(self):
        self.ingreso_neto_dispersion = sum(
            line.ingreso_neto for line in self.prenomina_line)

    @api.depends('prenomina_line.imss_patronal', 'prenomina_line.infonavit')
    def _compute_aportacion_patronal(self):
        total_imss = sum(
            line.imss_patronal for line in self.prenomina_line)
        total_infonavit = sum(
            line.infonavit for line in self.prenomina_line)
        self.impuestos_aportacion_patronal = total_imss + total_infonavit

    @api.depends('subtotal_ingreso', 'comision_nomina', 'impuestos_aportacion_obrera', 'ingreso_neto_dispersion', 'impuestos_aportacion_patronal')
    def _compute_total_deposito_nomina(self):
        self.total_deposito_nomina = self.subtotal_ingreso+self.comision_nomina + \
            self.impuestos_aportacion_obrera+self.ingreso_neto_dispersion + \
            self.impuestos_aportacion_patronal

    @api.depends('total_deposito_nomina', 'flujo_efectivo_deposito')
    def _compute_total_totales(self):
        self.total_totales = self.total_deposito_nomina+self.flujo_efectivo_deposito

    @api.depends('total_totales')
    def _compute_subtotal_co(self):
        self.subtotal_co = self.total_totales/1.16

    @api.depends('subtotal_co', 'total_totales')
    def _compute_iva_oc(self):
        self.iva_oc = self.total_totales - self.subtotal_co


class PrenominaComisionLine(models.Model):
    _name = "prenomina.comision.line"
    _description = "Detalle de prenomina"

    name = fields.Many2one('res.users', string='Usuario', required=True)

    # producto_id = fields.Many2one(
    #     'product.product', string='Producto asociado')

    cc_info = fields.Selection(
        [('imss', 'IMSS'), ('freelance', 'Freelance')], 'CC')

    salario = fields.Float(string='Salario')

    comisiones = fields.Float(string='Comisiones')

    bonos = fields.Float(string='Bonos')

    deducciones = fields.Float(string='Deducciones')

    comision_diez = fields.Float(  # Originalmente era diez, posteriormente se hizo configurable
        string='Comisión %', compute='_default_comision_diez')

    subtotal = fields.Float(string='Subtotal', compute='_default_subtotal')

    imss_obrera = fields.Float(string='IMSS (aportación obrera)')

    isr = fields.Float(string='ISR (aportación obrera)')

    ingreso_neto = fields.Float(
        string='Ingreso Neto', compute='_default_importe_neto')

    imss_patronal = fields.Float(string='IMSS (aportación patronal)')

    infonavit = fields.Float(string='INFONAVIT (aportación patronal)')

    prenomina_id = fields.Many2one('prenomina.comision', string="Prenomina",
                                   copy=False)

    rendimiento = fields.Float(string='Rendimiento')

    comision_pago_line = fields.One2many(comodel_name='comisiones.pagos',
                                         inverse_name='prenomina_line_id',
                                         string="Líneas de comisiones-pagos")

    @api.depends('salario', 'comisiones', 'bonos', 'deducciones')
    def _default_subtotal(self):
        for record in self:
            record.write({'subtotal': record.salario + record.comisiones +
                          record.bonos + record.deducciones})

    @api.depends('subtotal', 'imss_obrera', 'isr')
    def _default_importe_neto(self):
        for record in self:
            record.write(
                {'ingreso_neto': record.subtotal-(record.imss_obrera + record.isr)})

    @api.depends('subtotal')
    def _default_comision_diez(self):
        configuracion_comision = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1).porcentaje_comision_out
        for record in self:
            record.write(
                {'comision_diez': record.subtotal * (configuracion_comision / 100)})  # Convertir a porcentaje el dato de configuración
