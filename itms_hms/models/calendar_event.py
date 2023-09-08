# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, Command


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    name = fields.Char('Meeting Subject', required=True)
    STATE_SELECTION = [('pending', 'Pending Confirmation'),
                       ('confirmed', 'Confirmed'),
                       ('treated', 'Treated'),
                       ('cancelled', 'Cancelled')]
    patient_id = fields.Many2one('hms.patient', string='Patient')
    start_at = fields.Date('Date', default=fields.Date.today)
    physician_id = fields.Many2one('hms.physician', string='Prescriber')
    state = fields.Selection(STATE_SELECTION, string='Appointment Status', default='pending',
                             help="Status of the attendee's participation")
    consultation_type = fields.Many2one('hms.appointment',
                                        required=True, string='Consultation Type')
    consultation_service = fields.Many2one('product.product', string='Consultation Service')
    time_slot = fields.Many2one('appointment.schedule.slot.lines', string='Available Slots')
    payment_state = fields.Selection([('not_paid', 'Not Paid'),
                                      ('in_payment', 'In Payment'),
                                      ('paid', 'Paid')], default='not_paid', string='Payment Status')

    def write(self, values):
        if 'physician_id' in values:
            self.sudo().write(
                {'partner_ids': [
                    (6, 0, [self.env.user.partner_id.id, values.get('physician_id'), values.get('patient_id')])]})
        res = super().write(values)
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            self.name = self.patient_id.partner_id.name
