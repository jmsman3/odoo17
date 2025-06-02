# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    pur_req_id = fields.Many2one('cus.purchase.requisition', related='order_id.pur_req_id')
    parent_state = fields.Selection('Purchase State', related='order_id.state')


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    pur_req_id = fields.Many2one('cus.purchase.requisition', string="Purchase Requisition No")

    @api.onchange('pur_req_id')
    def _onchange_pur_req_id(self):
        for rec in self:
            if rec.pur_req_id:
                rec.picking_type_id = rec.pur_req_id.picking_type_id

                rec.order_line = [(5, 0, 0)]
                new_lines = []
                for line in rec.pur_req_id.order_line_ids:
                    new_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'product_qty': line.quantity,
                        'product_uom': line.product_id.uom_id.id,
                        'price_unit': line.price_unit,
                        'date_planned': rec.pur_req_id.req_date,
                        'name': line.name,
                    }))
                rec.order_line = new_lines
            else:
                rec.order_line = [(5, 0, 0)]

