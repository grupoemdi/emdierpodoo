# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import api
from odoo.exceptions import UserError

class ComisionesPagos(models.Model):
    _name = "comisiones.pagos"
    _description = "Comisiones relacionadas a los pagos"

    name = fields.Many2one(
        'sale.order', string='Orden de Venta', required=True)

    factura_id = fields.Many2one(
        'account.move', string='Factura')

    pago_id = fields.Many2one(
        'account.payment', string='Pago')

    #amount = fields.Monetary(string='Importe', related='pago_id.amount')
    currency_id = fields.Many2one(related='pago_id.currency_id')

    # factura_amount_total = fields.Monetary(
    #     string='Monto total de factura', related='factura_id.amount_total')

    fecha = fields.Date(string='Fecha de pago', related='pago_id.payment_date')

    porcentaje_factura = fields.Float(
        string='Porcentaje relativo a factura')

    comision_pago = fields.Float(string='Pago por comision')

    rendimiento_pago = fields.Float(string='Pago por rendimiento')

    comercial = fields.Many2one('res.users', string='Comercial')

    procesado = fields.Boolean(default=False, string='Se ha procesado en prenomina')

    prenomina_line_id = fields.Many2one('prenomina.comision.line', string='Línea de prenómina')


class ComisionPayment(models.Model):
    _inherit = 'account.payment'

    # @api.model
    # def create(self, vals):
    #     pago = super(ComisionPayment, self).create(vals)
    #     self._get_comisiones_pago_data(pago)
    #     return pago
    
    def post(self):
        print("en post")
        pago = super(ComisionPayment, self).post()
        self._get_comisiones_pago_data()
        return pago

    # def _get_comisiones_pago_data(self, pago_d):
    #     print('CREANDO REGISTRO COMISION::::')
    #     for record in pago_d.invoice_ids:
    #         porcentaje_factura = (pago_d.amount * 100) / record.amount_untaxed

    #         orden = self.env['sale.order'].search(
    #             [('name', '=', record.invoice_origin)], limit=1)

    #         comision_pago = (orden.x_comision * porcentaje_factura) / 100

    #         comision_pago_values = {
    #             'name': orden.id,
    #             'factura_id': record.id,
    #             'pago_id': pago_d.id,
    #             'fecha': pago_d.payment_date,
    #             'porcentaje_factura': porcentaje_factura,
    #             'comision_pago': comision_pago
    #         }
    #         self.env['comisiones.pagos'].create(comision_pago_values)

    def _get_comisiones_pago_data(self):
        print('CREANDO REGISTRO COMISION::::')
        #La siguiente configuración se elimina ya que siempre se generará el registro en comisión pago
        # configuracion = self.env['configuracion.comisiones'].search(
        #     [('id', '!=', 0)], limit=1)
        # if configuracion.metodo_pago_inmediato:
        #     metodo_inmediato = configuracion.metodo_pago_inmediato
        # else:
        #     raise UserError(
        #         'Pago: No hay configuración de pago inmediato en Ventas->Configuración->Comisiones')

        for record in self.invoice_ids:
            #if record.invoice_payment_term_id.id != metodo_inmediato.id:
            porcentaje_factura = (self.amount * 100) / record.amount_total
            orden = self.env['sale.order'].search(
                [('name', '=', record.invoice_origin)], limit=1)

            comision_pago = (orden.x_comision * porcentaje_factura) / 100
            rendimiento_pago = (orden.x_rendimiento * porcentaje_factura) / 100

            comision_pago_values = {
                'name': orden.id,
                'factura_id': record.id,
                'pago_id': self.id,
                'fecha': self.payment_date,
                'porcentaje_factura': porcentaje_factura,
                'comision_pago': comision_pago,
                'rendimiento_pago': rendimiento_pago,
                'comercial' : orden.user_id.id
            }
            self.env['comisiones.pagos'].create(comision_pago_values)
