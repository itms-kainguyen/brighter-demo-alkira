from odoo import models, fields, api, _
from odoo.tools import get_lang

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    delivery_note = fields.Text(string='Delivery Note')

    def prepare_line_notes(self, so_lines):
        #this function take the input of a source purchase order line (with product)
        #and create a note line for each partner in the sale order
        #find associated sale order line link to this purchase order line
        self.ensure_one()
        for line in self:
            related_so_lines = so_lines.filtered(lambda x: x.product_id == line.product_id)
            if related_so_lines:
                partner_quantity = {}
                for so_line in related_so_lines:
                    if so_line.order_partner_id in partner_quantity:
                        partner_quantity[so_line.order_partner_id] += so_line.product_uom_qty
                    else:
                        partner_quantity[so_line.order_partner_id] = so_line.product_uom_qty
                if partner_quantity:
                    notes = ''
                    for partner in partner_quantity:
                        notes += '%s deliver to %s\n' % (partner_quantity[partner], partner._display_address())
            return notes

    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        if 'product_id' in vals or 'product_qty' in vals:
            for line in self:
                sale_lines = self.move_dest_ids.group_id.sale_id | self.move_ids.move_dest_ids.group_id.sale_id
                if sale_lines:
                    sale_lines = sale_lines.mapped('order_line').filtered(lambda x: x.product_id == line.product_id)
                note = line.prepare_line_notes(sale_lines)
                if note:
                    line.delivery_note = note
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(PurchaseOrderLine, self).create(vals_list)
        for line in self:
            sale_lines = self.move_dest_ids.group_id.sale_id | self.move_ids.move_dest_ids.group_id.sale_id
            if sale_lines:
                sale_lines = sale_lines.mapped('order_line').filtered(lambda x: x.product_id == line.product_id)
            note = line.prepare_line_notes(sale_lines)
            if note:
                line.delivery_note = note
        return res