# -*- coding: utf-8 -*-

from datetime import date
from odoo import api
from odoo import models
from odoo import fields


class DialogoConfirmar(models.TransientModel):
    _name = 'dialogo.confirmar'
    _description = 'Dialogo Confirmar'

    text = fields.Char(string="Texto Confirmar", )

    def dialogo_confirmar_metodo(self):
        print("Confirmar")
