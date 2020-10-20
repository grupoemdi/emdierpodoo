# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class SOLinesValues(models.Model):
    _inherit = 'sale.order.line'


    #Campos
    x_precio_base = fields.Float(
        string='Precio Base')
    x_porcentaje_utilidad = fields.Float(
        string='% Utilidad deseada')
    x_precio_unidad = fields.Float(string='Precio deseado')

    @api.onchange('qty_delivered')
    def efecto_qty_delivered(self):
        print(self.qty_delivered,'Por favor funciona no mames tiraparo')



    # si se cambia el porcentaje de utilidad se cambia el precio unitario
    @api.onchange('x_porcentaje_utilidad')
    def get_price(self):
        print('cambia porcentaje')
        if self.x_porcentaje_utilidad < 0:
            raise ValidationError('Valor de utilidad no debe ser menor a 0')
        self.write({'price_unit': self.x_precio_base +
                    (self.x_precio_base*(self.x_porcentaje_utilidad/100))})

    # si se cambia el precio, se cambia el porcentaje de utilidad
    @api.onchange('x_precio_unidad')
    def get_precio_unitario(self):
        print('cambia x_precio unidad')
        if self.x_precio_base != 0:
            self.x_porcentaje_utilidad = (
                self.x_precio_unidad * 100 / self.x_precio_base)-100
    
    # si se cambia el descuento, se verifica que el precio no sea menor al precio base
    @api.onchange('discount')
    def check_desc_value(self):
        print('cambia descuento')
        if (self.price_subtotal/self.product_uom_qty) < self.x_precio_base:
            raise ValidationError('Precio después de descuento es inferior a precio base, ajusta porcentajes o descuento')

    # si se cambia la cantidad el precio unitario debe permanecer
    @api.onchange('product_uom_qty')
    def reset_utilidad(self):
        print('cambia cantidad')
        self.write({'x_porcentaje_utilidad': 0 })

    #TODO llamar al método de la clase padre
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(
            name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)

        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False
        ##INICIA EXTRA CALCS ##### READD
        self.write({'x_precio_base': self.price_unit})
        self.write({'x_porcentaje_utilidad': 0})
        #####FIN EXTRA CALCS #####
        return result

    #TODO llamar al método de la clase padre
    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )

            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
            
            ##INICIA EXTRA CALCS ##### READD
            self.write({'x_precio_base': self.price_unit})
            self.write({'x_porcentaje_utilidad': 0})
            #####FIN EXTRA CALCS #####

class SOValues(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res_id = super(SOValues, self).write(vals)
        for line in self.order_line:
            utilidad = line.x_porcentaje_utilidad
            line.x_precio_unidad = 0
            line.x_porcentaje_utilidad = utilidad
        return res_id

