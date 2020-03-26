# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import api

class ProjectTask(models.Model):
    _inherit = 'calendar.event'

    x_planta_id = fields.Many2one(
        'res.partner',
        string = 'Planta'
    )
    