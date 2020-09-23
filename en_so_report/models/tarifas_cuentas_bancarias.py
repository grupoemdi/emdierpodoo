# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import api
from odoo.exceptions import UserError


class TarifasListBanco(models.Model):
    _name = 'tarifas.cuentas.bancarias'
    _description = "Tarifas y Cuentas Bancarias"

    name = fields.Many2one('product.pricelist', string='Tarifa')
    cuenta_bancaria = fields.Many2one('res.partner.bank', string ='Cuenta Bancaria')
    
class TarifasRelacion(models.Model):
    _inherit = 'product.pricelist'

    x_cuenta_default = fields.Many2one('res.partner.bank', compute='get_respartnerbank')

    @api.depends('name')
    def get_respartnerbank(self):
        for record in self:
            tarifa_cuenta = self.env['tarifas.cuentas.bancarias'].search(
                [('name', '=', record.id)], limit=1)
            if tarifa_cuenta:
                print("Encontrado",tarifa_cuenta.name)
                record.x_cuenta_default = tarifa_cuenta.id
            else:
                record.x_cuenta_default = False
                
