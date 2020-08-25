# -*- coding: utf-8 -*-

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class SaleOrderAdds(models.Model):
    _inherit = 'sale.order'

    def default_costo_financiamiento(self):
        configuracion = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1)
        print('default configuracion',configuracion.name)
        if configuracion:
            return configuracion.costo_financiamiento
        else:
            return 0

    def action_delault_firma(self):
        return self.partner_id.signature

    @api.depends('x_porcentaje_utilidad')
    def _compute_porcentaje_utilidad(self):
        for record in self:
            record.x_porcentaje_utilidad_widget = record.x_porcentaje_utilidad * 100

    x_costo_financiamiento = fields.Float(
        string='Costo de financiamiento', default=default_costo_financiamiento)
    x_rendimiento = fields.Float(
        string='Rendimiento')
    x_comision = fields.Float(
        string='Comisión')
    x_equivalencia = fields.Float(
        string='Equivalencia')
    x_compra_asociada = fields.Text(string="Ordenes de compra asociadas")
    y_purchase_order_ids = fields.One2many('purchase.order',
                                         'y_sale_order_id')
    x_utilidad_bruta = fields.Float(string='Utilidad bruta')
    x_utilidad_venta = fields.Float(string='Utilidad de venta')
    x_porcentaje_utilidad = fields.Float(string='% Utilidad real')
    # este campo sólo se utiliza para mostar el valor en formato de porcentaje
    x_porcentaje_utilidad_widget = fields.Float(
        string='% Utilidad', compute='_compute_porcentaje_utilidad')
    x_utilidad_emdi = fields.Float(
        string='Utilidad EMDI')

    #x_studio_firma_del_vendedor = fields.Binary()




    def action_confirm(self):
        configuracion_limite = self.env['configuracion.comisiones'].search(
            [('id', '!=', 0)], limit=1).limite_confirmar_venta

        if self.amount_total >= configuracion_limite:
            if self.is_group_supervisor == False:
                raise ValidationError(
                    'El monto de la Orden requiere confirmación de Supervisor')
        return super(SaleOrderAdds, self).action_confirm()

    # @api.one
    def _compute_is_group_supervisor(self):
        self.ensure_one()
        self.is_group_supervisor = self.env['res.users'].has_group(
            'en_comisiones.group_supervisor_ventas')

    # Campo para revisar si el usuario actual es un administrador
    is_group_supervisor = fields.Boolean(
        string='Es supervisor',
        compute="_compute_is_group_supervisor",
    )


    @api.onchange('payment_term_id')
    def _onchange_payment_term_id(self):
        print(self.payment_term_id.name)
        if self.payment_term_id.name == 'Pago de contado':
            print("Ceros################")
            self.x_costo_financiamiento = 0
            return
        else:
            print('tres%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            self.x_costo_financiamiento = 3
            return
        self.x_costo_financiamiento = 0

    def _action_confirm(self):
        #print("PPPPPPPPPPPPPPPPPPPPPPPPPPP")
        """ Generate inter company purchase order based on conditions """
        res = super(SaleOrderAdds, self)._action_confirm()
        ordenes_de_compra = self.env['purchase.order'].search(
            [('origin', '=', self.name)])
        i = 0
        for purcharse_order in ordenes_de_compra:
            #print(purcharse_order.name,"YYYYYYYYYYYYYYYY")
            purcharse_order.write({'y_sale_order_id': self.id})
            if i == 0:
                self.x_compra_asociada = purcharse_order.name
                i += 1
            else:
                self.x_compra_asociada += ','+purcharse_order.name
        return res

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        orden_venta = super(SaleOrderAdds, self).copy(default=default)
        orden_venta.x_rendimiento = 0
        orden_venta.x_comision = 0
        orden_venta.x_equivalencia = 0
        orden_venta.x_utilidad_bruta = 0
        orden_venta.x_utilidad_venta = 0
        orden_venta.x_porcentaje_utilidad = 0
        orden_venta.x_utilidad_emdi = 0
        orden_venta.x_compra_asociada = ""
        return orden_venta


    # def inter_company_create_purchase_order(self, company):
    #     print("#############################################################")
    #     """ Create a Purchase Order from the current SO (self)
    #         Note : In this method, reading the current SO is done as sudo, and the creation of the derived
    #         PO as intercompany_user, minimizing the access right required for the trigger user
    #         :param company : the company of the created PO
    #         :rtype company : res.company record
    #     """
    #     self = self.with_context(force_company=company.id, company_id=company.id)
    #     PurchaseOrder = self.env['purchase.order']
    #     PurchaseOrderLine = self.env['purchase.order.line']
    #
    #     for rec in self:
    #         if not company or not rec.company_id.partner_id:
    #             continue
    #
    #         # find user for creating and validating SO/PO from company
    #         intercompany_uid = company.intercompany_user_id and company.intercompany_user_id.id or False
    #         if not intercompany_uid:
    #             raise Warning(_('Provide one user for intercompany relation for % ') % company.name)
    #         # check intercompany user access rights
    #         if not PurchaseOrder.with_user(intercompany_uid).check_access_rights('create', raise_exception=False):
    #             raise Warning(_("Inter company user of company %s doesn't have enough access rights") % company.name)
    #
    #         company_partner = rec.company_id.partner_id.with_user(intercompany_uid)
    #         # create the PO and generate its lines from the SO
    #         # read it as sudo, because inter-compagny user can not have the access right on PO
    #         po_vals = rec.sudo()._prepare_purchase_order_data(company, company_partner)
    #         inter_user = self.env['res.users'].sudo().browse(intercompany_uid)
    #         purchase_order = PurchaseOrder.with_context(allowed_company_ids=inter_user.company_ids.ids).with_user(intercompany_uid).create(po_vals)
    #         for line in rec.order_line.sudo():
    #             po_line_vals = rec._prepare_purchase_order_line_data(line, rec.date_order,
    #                 purchase_order.id, company)
    #             # TODO: create can be done in batch; this may be a performance bottleneck
    #             PurchaseOrderLine.with_user(intercompany_uid).with_context(allowed_company_ids=inter_user.company_ids.ids).create(po_line_vals)
    #
    #         # write customer reference field on SO
    #         if not rec.client_order_ref:
    #             rec.client_order_ref = purchase_order.name
    #
    #         # auto-validate the purchase order if needed
    #         if company.auto_validation:
    #             purchase_order.with_user(intercompany_uid).button_confirm()
    #
    #
    #
    # def _prepare_purchase_order_data(self, company, company_partner):
    #     print("overidde metod")
    #     """ Generate purchase order values, from the SO (self)
    #         :param company_partner : the partner representing the company of the SO
    #         :rtype company_partner : res.partner record
    #         :param company : the company in which the PO line will be created
    #         :rtype company : res.company record
    #     """
    #     self.ensure_one()
    #     # find location and warehouse, pick warehouse from company object
    #     PurchaseOrder = self.env['purchase.order']
    #     warehouse = company.warehouse_id and company.warehouse_id.company_id.id == company.id and company.warehouse_id or False
    #     if not warehouse:
    #         raise Warning(_(
    #             'Configure correct warehouse for company(%s) from Menu: Settings/Users/Companies' % (
    #                 company.name)))
    #     picking_type_id = self.env['stock.picking.type'].search([
    #         ('code', '=', 'incoming'), ('warehouse_id', '=', warehouse.id)
    #     ], limit=1)
    #     if not picking_type_id:
    #         intercompany_uid = company.intercompany_user_id.id
    #         picking_type_id = PurchaseOrder.with_user(
    #             intercompany_uid)._default_picking_type()
    #     return {
    #         'name': self.env['ir.sequence'].sudo().next_by_code(
    #             'purchase.order'),
    #         'origin': self.name,
    #         'partner_id': company_partner.id,
    #         'picking_type_id': picking_type_id.id,
    #         'date_order': self.date_order,
    #         'company_id': company.id,
    #         'fiscal_position_id': company_partner.property_account_position_id.id,
    #         'payment_term_id': company_partner.property_supplier_payment_term_id.id,
    #         'auto_generated': True,
    #         'auto_sale_order_id': self.id,
    #         'partner_ref': self.name,
    #         'currency_id': self.currency_id.id,
    #         'y_sale_order_id': self.id
    #     }



class purchaseOrderComisiones(models.Model):
    _inherit = 'purchase.order'

    y_sale_order_id = fields.Many2one(
        'sale.order', string='Orden de venta asociada')


