# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class appointment_booking(models.Model):
    _name = 'appointment'
    _description = 'appointment'

    @api.model
    def _get_default_appointment_group_id(self):
        return self.env['appointment.group'].search(
            [('product_template_id.name', '=', 'Prescriber Service')], limit=1) or False

    customer = fields.Many2one('res.partner', string='Patient')
    appointment_group_id = fields.Many2one('appointment.group',  default=_get_default_appointment_group_id, string='Consultation Type')
    appoint_person_id = fields.Many2one('res.partner', string='Prescriber')
    time_slot = fields.Many2one('appointment.timeslot', string='Available Slots')
    appoint_date = fields.Date(string="Date")
    source = fields.Many2one('appointment.source', string='Source')
    create_date = fields.Datetime(string='Create Date')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Text()
    price_unit = fields.Float()
    tax_id = fields.Many2many('account.tax', string='Tax')
    price_subtotal = fields.Float(string='Subtotal')
    address_id = fields.Char(string='Address')
    email_id = fields.Char(string='Email')
    mobile_number = fields.Char(string='Mobile Number')
    remark = fields.Text(string='Remarks')
    state = fields.Selection([('pending', 'Pending Confirmation'),
                              ('confirmed', 'Submit'),
                              ('treated', 'Treated'),
                              ('cancelled', 'Cancelled')], default='pending', string='Status')

    def action_confirm(self):
        return self.write({'state': 'confirmed'})

    def action_cancel(self):
        return self.write({'state': 'cancelled'})

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_default_nurse(self):
        if self.env.user.partner_id.position_type == 'Nurses':
            return self.env.user.partner_id
        return self.env['res.partner'].search(
            [('position_type', '=', 'Nurses'), ('company_id', '=', self.env.user.company_id.id)], limit=1)

    @api.model
    def _get_default_company(self):
        return self.env.user.company_id

    last_name = fields.Char(string='Last name', )
    full_name = fields.Char(string='Last name', compute='_compute_fullname', store=True)
    appointment_group_ids = fields.Many2many('appointment.group', string='Consultation Type')
    title = fields.Many2one('res.partner.title', string='Title')
    appointment_charge = fields.Float(string='Appointment Charge')
    appoint_product_id = fields.Many2one('product.template', string='Appointee Product')
    work_exp = fields.Char(string='Work Experience')
    specialist = fields.Char(string='Specialist')
    slot_ids = fields.Many2many('calendar.appointment.slot')
    appointment_type = fields.Many2one('calendar.appointment.type', string="Appointment Type")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', )
    start_datetime = fields.Datetime(string="Appointment Date")
    doctor_id = fields.Many2one('res.partner', 'Prescriber')
    # nurses_id = fields.Many2one('res.users', domain="[('position_type', '=', 'Nurses'),('company_id', '=',
    # company_id)]", string='Nurses')
    nurses_id = fields.Many2one('res.partner', readonly="1",
                                domain="[('position_type', '=', 'Nurses'),('company_id', '=', company_id)]",
                                default=_get_default_nurse,
                                string='Nurses')
    birth_date = fields.Date('Birth Date')
    allergies = fields.Selection([('none', 'None'),
                                  ('Bees /wasps', 'Bees /wasps'),
                                  ('Penicillin', 'Penicillin'),
                                  ('Hylase', 'Hylase'),
                                  ('Anaesthetic', 'Anaesthetic'),
                                  ('Latex', 'Latex'),
                                  ('Other', 'Other'),
                                  ('Paracetamol', 'Paracetamol'),
                                  ('Sulphur', 'Sulphur'),
                                  ('Maxalon', 'Maxalon'),
                                  ('Stemetil', 'Stemetil'),
                                  ('Vaccination', 'Vaccination'),
                                  ('Boosters', 'Boosters'),
                                  ('Peanuts', 'Peanuts')], default='none', string='Allergies')
    blood_group = fields.Char(string='Blood Group')
    sex = fields.Selection([('Female', 'Female'), ('Male', 'Male')], string='Sex')
    provider = fields.Char(string='Provider')
    prescriber = fields.Char(string='Prescriber')
    position_type = fields.Selection([('Prescriber', 'Prescriber'), ('Nurses', 'Nurse'), ('Patient', 'Patient')],
                                     default='Patient',
                                     string='Position Type')

    appointment_ids = fields.One2many('appointment', 'appoint_person_id', string='Appointment')
    appointment_patient_ids = fields.One2many('appointment', 'customer', string='History')
    password = fields.Char(string='Password')
    age = fields.Integer(compute='_compute_age', string='Age')
    company_id = fields.Many2one('res.company', default=_get_default_company, string='Company',
                                 index=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            rec.age = 0
            if rec.birth_date:
                rec.age = datetime.now().year - rec.birth_date.year

    @api.depends('last_name')
    def _compute_fullname(self):
        for rec in self:
            rec.full_name = ('%s  %s' % (rec.name or '', rec.last_name or '')) or ''

    @api.onchange('appointment_type')
    def _onchange_parnter(self):
        partner = self.env['calendar.appointment.type'].sudo().search([('name', '=', self.appointment_type.name)])
        self.slot_ids = partner.slot_ids

    def calendar_verify_availability(self, date_start, date_end):
        """ verify availability of the partner(s) between 2 datetimes on their calendar
        """
        if bool(self.env['calendar.event'].search_count([
            ('partner_ids', 'in', self.ids),
            '|', '&', ('start_datetime', '<', fields.Datetime.to_string(date_end)),
            ('stop_datetime', '>', fields.Datetime.to_string(date_start)),
            '&', ('allday', '=', True),
            '|', ('start_date', '=', fields.Date.to_string(date_end)),
            ('start_date', '=', fields.Date.to_string(date_start))])):
            return False
        return True
