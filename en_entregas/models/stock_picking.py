# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import smtplib

class StockPickingMods(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('scheduled_date')
    def valida_grupo(self):
        if self.is_in_group == False:
            raise ValidationError(
                'Usuario actual no puede modificar Fecha Prevista')
        print(self.x_motivo_modificacion)
        if not self.x_motivo_modificacion: #if not proyecto:
            #self._envia_correos()
            raise ValidationError(
                'Para modificar campo de Fecha primero se debe seleccionar una Razón de cambio en fecha')
        
    #TODO: Esta validación se podría saltar si el usuario cambia fecha prevista y después borra la razón de cambio
    @api.onchange('x_motivo_modificacion') 
    def valida_grupo_motivo(self):
        if self.is_in_group == False:
            raise ValidationError(
                'Usuario actual no puede modificar Razón de cambio en fecha')

    @api.onchange('x_comentarios')
    def valida_grupo_comentarios(self):
        if self.is_in_group == False:
            raise ValidationError(
                'Usuario actual no puede modificar Comentarios')

    def _compute_is_group_mods(self):
        self.is_in_group = self.env['res.users'].has_group(
            'en_entregas.group_supervisor_movimientos')
    
    def _envia_correos(self): #Validaciones, si algún miembro no tiene correo, si hay servidores configurados
        print("Ejecutando enviar")

        self.sudo() # Este es el Super Usuario Odoo
        #self.env['res.partner'].sudo().create({vals})
        servidor_salida=self.env['ir.mail_server'].sudo().search([], limit=1)
        
        #obtener datos del cuerpo del mensaje
        nombre_movimiento = self.name or ''
        fecha_prevista = str(self.scheduled_date) or ''
        razon_cambio = self.x_motivo_modificacion.name or ''
        razon_cambio = razon_cambio.encode('ascii', 'ignore').decode('ascii')
        comentarios = self.x_comentarios or ''
        comentarios = comentarios.encode('ascii', 'ignore').decode('ascii')
        for seguidor in self.message_follower_ids:
            receivers=""
            message = """\
                Cambio en registro de Fecha Prevista

                """
            sender = servidor_salida.smtp_user
            receivers = seguidor.partner_id.email
            if receivers != False:
                receivers = receivers.encode('ascii', 'ignore').decode('ascii') #si el correo tiene caracteres no validos
                if (re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',receivers.lower())): #Correo correcto validado como expresion
                    print("::::",seguidor.partner_id.name)
                    message += "Estimado usuario " + seguidor.partner_id.name + ", se ha actualizado el registro de entregas con los siguientes datos "
                    message += "\n" + "Movimiento: " + nombre_movimiento
                    message += "\n" + "Nueva Fecha/Hora: " + fecha_prevista
                    message += "\n" + "Motivo de cambio en fecha: " + razon_cambio
                    message += "\n" + "Comentarios: " + comentarios

                    smtpObj = smtplib.SMTP(host=servidor_salida.smtp_host, port=servidor_salida.smtp_port)
                    print("paso1")
                    smtpObj.ehlo()
                    print("paso2")
                    smtpObj.starttls()
                    print("paso3")
                    smtpObj.ehlo()
                    print("paso4")
                    smtpObj.login(user=servidor_salida.smtp_user, password=servidor_salida.smtp_pass)
                    print("paso5")
                    smtpObj.sendmail(sender, receivers, message)
                    print ("Correo enviado")
                else:
                    print ("Correo incorrecto")

    is_in_group = fields.Boolean(
        string='Puede modificar',
        compute="_compute_is_group_mods",
    )

    x_comentarios = fields.Text(
        string='Cometarios'
    )

    x_motivo_modificacion = fields.Many2one(
        'causa.cambio', string='Razón de cambio en fecha')

    x_historial_ids = fields.One2many(comodel_name='historial.fechas',
                                  inverse_name='picking_id',
                                  string="Cambios de fecha")

    def write(self, vals):
        if 'scheduled_date' in vals:
            usuario = self.env.user.id
            fecha_anterior= self.scheduled_date
            res_id = super(StockPickingMods, self).write(vals)
            historial_data={
                'name': usuario,
                'fecha_anterior': fecha_anterior,
                'fecha_actualizada': self.scheduled_date,
                'motivo_modificacion': self.x_motivo_modificacion.id,
                'comentarios': self.x_comentarios,
                'picking_id': self.id,
            }
            historico = self.env['historial.fechas'].create(historial_data)
            self._envia_correos()
        else:
            res_id = super(StockPickingMods, self).write(vals)
        return res_id
