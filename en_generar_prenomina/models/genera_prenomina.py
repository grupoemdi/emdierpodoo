# -*- coding: utf-8 -*-

#from odoo import fields
#import calendar
from datetime import date
#from datetime import datetime
from odoo import api
from odoo import models
#from odoo.exceptions import UserError


class PrenominaComisiones(models.Model):
    _name = "prenomina.comisiones"
    _description = 'Generar prenomina'

    @api.model
    def prenomina_venta_comisiones(self):
        print("Ejecutando accion planificada Creando Prenomina")
        #fecha_actual = datetime.now().date().year
        fecha_actual = date.today()
        prenomina_data={
            'name' : 'Prenómina con fecha: ' + str(fecha_actual)
        }
        prenomina_creada = self.env['prenomina.comision'].create(prenomina_data)
        prenomina_creada.get_data_comision()
        print('Fin Prenomina creada')
