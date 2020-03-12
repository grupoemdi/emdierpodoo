# -*- coding: utf-8 -*-

from odoo import models, fields

class CuentasEnTarifas(models.Model):
    _inherit = 'product.pricelist'

    x_cuenta_bancaria = fields.Many2one('res.partner.bank', string = 'Cuenta Bancaria')
