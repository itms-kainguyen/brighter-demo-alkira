# -*- coding: utf-8 -*-
from odoo import api, fields, models
import json


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    document_type = fields.Selection([
        ('bedroom1', 'Bedroom 1'),
        ('bedroom2', 'Bedroom 2'),
        ('bedroom3', 'Bedroom 3'),
        ('bedroom4', 'Bedroom 4'),
        ('bedroom5', 'Bedroom 5'),
        ('bedroom6', 'Bedroom 6'),
        ('bedroom7', 'Bedroom 7'),
        ('bedroom8', 'Bedroom 8'),
        ('butlers_pantry', 'Butlers Pantry'),
        ('dining_room', 'Dining Room'),
        ('entry', 'Entry'),
        ('games_room', 'Games Room'),
        ('guest_room', 'Guest Room'),
        ('hallway', 'Hallway'),
        ('kitchen', 'Kitchen'),
        ('landing', 'Landing'),
        ('linen_closet', 'Linen Closet'),
        ('living_room', 'Living Room'),
        ('lounge_room', 'Lounge Room'),
        ('master_bedroom', 'Master Bedroom'),
        ('master_bedroom Ensuite', 'Master Bedroom Ensuite'),
        ('master_bedroom W.I.R.', 'Master Bedroom W.I.R.'),
        ('media_room', 'Media Room'),
        ('play_room', 'Play Room'),
        ('prayer_room', 'Prayer Room'),
        ('room_1', 'Room 1'),
        ('room_2', 'Room 2'),
        ('room_3', 'Room 3'),
        ('room_4', 'Room 4'),
        ('stairs', 'Stairs'),
        ('study', 'Study'),
        ('mud_map', 'Mud Map'),
        ('plan', 'Plan'),
        ('stock_check_ok', 'Stock Check OK'),
        ('stock_check_notok', 'Stock Check NOT OK'),
        ('customer_approval', 'Customer Approval'),
        ('spiv', 'SPIV'),
        ('signed_invoice', 'Signed Invoice'),
        ('signed_mud_map', 'Signed Mud Map'),
        ('underlay_voucher', 'Underlay Voucher'),
        ('remittance_advice', 'Remittance Advice'),
        ('photo', 'Photo'),
        ('layers_plan', 'Layers Plan'),
        ('receipt', 'Receipt'),
        ('other', 'Other')
    ], string='Document Type')
    instruction_pdf = fields.Binary('PDF')
    file_display = fields.Binary('file')
    instruction_type = fields.Selection([
        ('pdf', 'PDF'), ('image', 'Image')],
        string="Instruction", default="image"
    )

    def action_remove_record(self):
        for rec in self:
            rec.unlink()
