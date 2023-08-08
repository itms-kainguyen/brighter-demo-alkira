# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.http import request
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class appointment_group(models.Model):
    _name = 'appointment.group'

    name = fields.Char(string='Group Name')
    appointment_charge = fields.Float(string='Appointment Charge', required=True)
    product_template_id = fields.Many2one('product.template', string='Group Product')
    appointment_group_ids = fields.Many2many('res.partner')
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', string='State', required=False,
                               domain="[('country_id', '=', country_id)]")
    currency_id = fields.Many2one(related="company_id.currency_id", string='Currency', readonly=False)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.model
    def get_count_list(self):
        total_service = self.env['appointment.group'].sudo().search_count([])
        total_appointment = request.env['calendar.event'].sudo().search_count([])
        pending_appointment = request.env['calendar.event'].sudo().search_count(
            [('attendee_ids.state', '=', 'needsAction')])
        approved_appointment = request.env['calendar.event'].sudo().search_count(
            [('attendee_ids.state', '=', 'accepted')])
        rejected_appointment = request.env['calendar.event'].sudo().search_count(
            [('attendee_ids.state', '=', 'declined')])
        today_appointment = request.env['calendar.event'].sudo().search_count([('start_at', '=', fields.Date.today())])
        patient_appointment = request.env['res.partner'].sudo().search_count([('position_type', '=', 'Patient')])
        if not self.env.user.has_group('doctor_appointment_booking_advance_axis.group_helpdesk_manager') and \
                not self.env.user.has_group('doctor_appointment_booking_advance_axis.group_helpdesk_admin') and \
                not self.env.user.is_admin():
            domain = [('position_type', '=', 'Patient'), ('nurses_id', '=', self.env.user.partner_id.id), '|',
                      ('doctor_id', '=', self.env.user.partner_id.id)]
            patient_appointment = request.env['res.partner'].sudo().search_count(domain)
            total_appointment = request.env['calendar.event'].sudo().search_count(
                [('user_id', '=', self.env.user.id), ('partner_ids', 'in', self.env.user.partner_id.id)])
        shop_appointment = request.env['product.template'].sudo().search_count([('is_published', '=', True)])

        return {
            'total_service': total_service,
            'total_appointment': total_appointment,
            'pending_appointment': pending_appointment,
            'approved_appointment': approved_appointment,
            'rejected_appointment': rejected_appointment,
            'today_appointment': today_appointment,
            'patient-appointment': patient_appointment,
            'shop-appointment': shop_appointment
        }

    def write(self, vals):
        res = super(appointment_group, self).write(vals)
        group_partner = self.appointment_group_ids.ids
        partner = self.env['res.partner'].search([('id', 'in', group_partner)])
        for rec in partner:
            if not partner.appointment_group_ids:
                rec.write({
                    'appointment_group_ids': self.id,
                })
        return res

    @api.model
    def create(self, vals):
        res = super(appointment_group, self).create(vals)
        group_partner = res.appointment_group_ids.ids
        partner = self.env['res.partner'].search([('id', 'in', group_partner)])
        for rec in partner:
            if not rec.appointment_group_ids:
                rec.write({
                    'appointment_group_ids': res.id,
                })
        return res
