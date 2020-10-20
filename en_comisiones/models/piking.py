# -*- coding: utf-8 -*-

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class EfectoStockPicking(models.Model):
    _inherit = 'stock.picking'

    efecto_counded_inv = fields.Integer(default=0)
