# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class ACSTreatment(models.Model):
    _name = 'hms.treatment'
    _description = "Treatment"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'acs.hms.mixin', 'acs.documnt.mixin']

    @api.depends('medical_alert_ids')
    def _get_alert_count(self):
        for rec in self:
            rec.alert_count = len(rec.medical_alert_ids)

    @api.model
    def _get_service_id(self):
        registration_product = False
        if self.env.user.company_id.treatment_registration_product_id:
            registration_product = self.env.user.company_id.treatment_registration_product_id.id
        return registration_product

    def _rec_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)
            rec.patient_procedure_count = len(rec.patient_procedure_ids)

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    name = fields.Char(string='Name', readonly=True, index=True, copy=False, tracking=True)
    subject = fields.Char(string='Subject', tracking=True, states=READONLY_STATES)
    patient_id = fields.Many2one('hms.patient', 'Patient', required=True, index=True, states=READONLY_STATES,
                                 tracking=True)
    department_id = fields.Many2one('hr.department', ondelete='restrict', string='Department',
                                    domain=[('patient_department', '=', True)], states=READONLY_STATES, tracking=True)
    image_128 = fields.Binary(related='patient_id.image_128', string='Image', readonly=True)
    date = fields.Datetime(string='Date of Treatment', default=fields.Datetime.now, states=READONLY_STATES)
    healed_date = fields.Date(string='Healed Date', states=READONLY_STATES)
    end_date = fields.Date(string='End Date', help='End of treatment date', states=READONLY_STATES)
    diagnosis_id = fields.Many2one('hms.diseases', string='Medicine', states=READONLY_STATES)
    nurse_id = fields.Many2one('res.users', 'Nurse', domain=[('physician_id', '=', False)], required=True)
    physician_id = fields.Many2one('hms.physician', ondelete='restrict', string='Prescriber', states=READONLY_STATES,
                                   tracking=True)
    attending_physician_ids = fields.Many2many('hms.physician', 'hosp_treat_doc_rel', 'treat_id', 'doc_id',
                                               string='Primary Doctors',
                                               states=READONLY_STATES)
    prescription_line_ids = fields.One2many('prescription.line', 'treatment_id', 'Prescription',
                                            states=READONLY_STATES)
    medicine_line_ids = fields.One2many('treatment.medicine.line', 'treatment_id', 'Medicine',
                                        states=READONLY_STATES)
    template_id = fields.Many2one('treatment.template', 'Template Note')
    finding = fields.Html(string="Findings", states=READONLY_STATES)
    appointment_ids = fields.One2many('hms.appointment', 'treatment_id', string='Appointments',
                                      states=READONLY_STATES)
    appointment_count = fields.Integer(compute='_rec_count', string='# Appointments')
    appointment_id = fields.Many2one("hms.appointment", string="Appointment")
    appointment_prescription_line_id = fields.Many2one('appointment.prescription.line', string="Appointment line")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', required=True, copy=False, states=READONLY_STATES, tracking=True)
    description = fields.Char(string='Treatment Description', states=READONLY_STATES)

    is_allergy = fields.Boolean(string='Allergic Disease', states=READONLY_STATES)
    pregnancy_warning = fields.Boolean(string='Pregnancy warning', states=READONLY_STATES)
    lactation = fields.Boolean('Lactation', states=READONLY_STATES)
    disease_severity = fields.Selection([
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ], string='Severity', index=True, states=READONLY_STATES)
    disease_status = fields.Selection([
        ('acute', 'Acute'),
        ('chronic', 'Chronic'),
        ('unchanged', 'Unchanged'),
        ('healed', 'Healed'),
        ('improving', 'Improving'),
        ('worsening', 'Worsening'),
    ], string='Status of the disease', index=True, states=READONLY_STATES)
    is_infectious = fields.Boolean(string='Infectious Disease', states=READONLY_STATES)
    allergy_type = fields.Selection([
        ('da', 'Drug Allergy'),
        ('fa', 'Food Allergy'),
        ('ma', 'Misc Allergy'),
        ('mc', 'Misc Contraindication'),
    ], string='Allergy type', index=True, states=READONLY_STATES)
    age = fields.Char(string='Age when diagnosed', states=READONLY_STATES)
    patient_disease_id = fields.Many2one('hms.patient.disease', string='Patient Disease', states=READONLY_STATES)
    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='restrict', copy=False)
    company_id = fields.Many2one('res.company', ondelete='restrict', states=READONLY_STATES,
                                 string='Clinic', default=lambda self: self.env.company)
    medical_alert_ids = fields.Many2many('acs.medical.alert', 'treatment_medical_alert_rel', 'treatment_id', 'alert_id',
                                         string='Medical Alerts', related="patient_id.medical_alert_ids")
    alert_count = fields.Integer(compute='_get_alert_count', default=0)
    registration_product_id = fields.Many2one('product.product', default=_get_service_id, string="Registration Service")
    department_type = fields.Selection(related='department_id.department_type', string="Treatment Department",
                                       store=True)

    patient_procedure_ids = fields.One2many('acs.patient.procedure', 'treatment_id', 'Patient Procedures')
    patient_procedure_count = fields.Integer(compute='_rec_count', string='# Patient Procedures')
    procedure_group_id = fields.Many2one('procedure.group', ondelete="set null", string='Procedure Group',
                                         states=READONLY_STATES)

    consumable_line_ids = fields.One2many('hms.consumable.line', 'treatment_id',
                                          string='Consumable Line', states=READONLY_STATES, copy=False)
    # photos
    attachment_before_ids = fields.Many2many('ir.attachment', 'treatment_attachment_before_rel', 'attachment_id',
                                             'treatment_id', string='Before Photos')
    attachment_after_ids = fields.Many2many('ir.attachment', 'treatment_attachment_after_rel', 'attachment_id',
                                            'treatment_id', string='After Photos')
    prescription_ids = fields.Many2many('prescription.order', 'prescription_treatment_rel', 'prescription_id', 'treatment_id',
                                        string='Prescriptions')
    available_prescription_ids = fields.Many2many('prescription.order', 'prescription_treatment_available_rel', 'prescription_id', 'treatment_id',
                                        string='Prescriptions', compute='_compute_available_prescription_ids')
    
    def action_unlink(self):
        self.ensure_one()
        appointment_id = self.appointment_id.id
        self.unlink()
        return {'name': f"Appointment",
                'view_mode': 'form',
                'res_model': 'hms.appointment',
                'view_id': self.env.ref('acs_hms.view_hms_appointment_form').id,
                'res_id': appointment_id,
                'type': 'ir.actions.act_window',
                }
    
    @api.depends('patient_id')
    def _compute_available_prescription_ids(self):
        for rec in self:
            rec.available_prescription_ids = self.env['prescription.order'].search([
                ('patient_id', '=', rec.patient_id.id), 
                ('state', '=', 'prescription')]
            )

    @api.onchange('prescription_ids')
    def onchange_prescription_ids(self):
        for rec in self:
            rec.medicine_line_ids = False
            prescription_line_ids = rec.prescription_ids.mapped('prescription_line_ids')
            for line in prescription_line_ids:
                if line.repeat > 0:
                    rec.medicine_line_ids = [(0, 0, {
                        'product_id': line.product_id.id,
                        'medicine_area': line.medicine_area,
                        'medicine_technique': line.medicine_technique,
                        'medicine_depth': line.medicine_depth,
                        'medicine_method': line.medicine_method,
                        'repeat': line.repeat,
                        'prescription_id': line.prescription_id.id,
                    })]
            
    @api.model
    def default_get(self, fields):
        res = super(ACSTreatment, self).default_get(fields)
        if self._context.get('acs_department_type'):
            department = self.env['hr.department'].search(
                [('department_type', '=', self._context.get('acs_department_type'))], limit=1)
            if department:
                res['department_id'] = department.id
        return res

    def action_view_patient_procedures(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms.action_acs_patient_procedure")
        action['domain'] = [('id', 'in', self.patient_procedure_ids.ids)]
        action['context'] = {'default_patient_id': self.patient_id.id, 'default_treatment_id': self.id,
                             'default_department_id': self.department_id.id}
        return action

    @api.onchange('department_id')
    def onchange_department(self):
        if self.department_id:
            self.department_type = self.department_id.department_type

    @api.onchange('template_id')
    def onchange_template_id(self):
        self.finding = None
        if self.template_id:
            self.finding = self.template_id.notes

    def get_line_data(self, line):
        base_date = fields.Date.today()
        return {
            'product_id': line.product_id.id,
            'patient_id': self.patient_id.id,
            'date': fields.datetime.now() + timedelta(days=line.days_to_add),
            'date_stop': fields.datetime.now() + timedelta(days=line.days_to_add) + timedelta(
                hours=line.product_id.procedure_time)
        }

    @api.onchange('procedure_group_id')
    def onchange_procedure_group(self):
        patient_procedure_ids = []
        if self.procedure_group_id:
            for line in self.procedure_group_id.line_ids:
                patient_procedure_ids.append((0, 0, self.get_line_data(line)))
            self.patient_procedure_ids = patient_procedure_ids
    
    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('name', 'New Treatment') == 'New Treatment':
                values['name'] = self.env['ir.sequence'].next_by_code('hms.treatment') or 'New Treatment'
        return super().create(vals_list)

    def unlink(self):
        for data in self:
            if data.state in ['done']:
                raise UserError(('You can not delete record in done state'))
        return super(ACSTreatment, self).unlink()

    def treatment_draft(self):
        self.state = 'draft'

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.age = self.patient_id.age

    def treatment_running(self):
        patient_disease_id = self.env['hms.patient.disease'].create({
            'patient_id': self.patient_id.id,
            'treatment_id': self.id,
            'disease_id': self.diagnosis_id.id,
            'age': self.age,
            'diagnosed_date': self.date,
            'healed_date': self.healed_date,
            'allergy_type': self.allergy_type,
            'is_infectious': self.is_infectious,
            'status': self.disease_status,
            'disease_severity': self.disease_severity,
            'lactation': self.lactation,
            'pregnancy_warning': self.pregnancy_warning,
            'is_allergy': self.is_allergy,
            'description': self.description,
        })
        self.patient_disease_id = patient_disease_id.id
        self.state = 'running'

    def treatment_done(self):
        self.state = 'done'
        self.appointment_prescription_line_id.is_done = True
        self.appointment_prescription_line_id.done_at = datetime.now()
        self.appointment_prescription_line_id.prescription_line_id.is_done = True
        self.appointment_prescription_line_id.prescription_line_id.done_at = datetime.now()
        if self.env.context.get('from_appointment'):
            return {'name': f"Appointment",
                    'view_mode': 'form',
                    'res_model': 'hms.appointment',
                    'view_id': self.env.ref('acs_hms.view_hms_appointment_form').id,
                    'res_id': self.appointment_id.id,
                    'type': 'ir.actions.act_window',
                    }

    def treatment_cancel(self):
        self.state = 'cancel'

    # def action_appointment(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("acs_hms.action_appointment")
    #     action['domain'] = [('treatment_id', '=', self.id)]
    #     action['context'] = {
    #         'default_treatment_id': self.id,
    #         'default_patient_id': self.patient_id.id,
    #         'default_physician_id': self.physician_id.id,
    #         'default_department_id': self.department_id and self.department_id.id or False}
    #     return action

    def action_appointment(self):
        return {'name': f"Appointment",
                'view_mode': 'form',
                'res_model': 'hms.appointment',
                'view_id': self.env.ref('acs_hms.view_hms_appointment_form').id,
                'res_id': self.appointment_id.id,
                'type': 'ir.actions.act_window',
                }

    def create_invoice(self):
        product_id = self.registration_product_id or self.env.user.company_id.treatment_registration_product_id
        acs_context = {'commission_partner_ids': self.physician_id.partner_id.id}
        product_data = []
        if self.medicine_line_ids:
            for line in self.medicine_line_ids:
                product_data.append({
                    'product_id': line.product_id
                })
        if self.consumable_line_ids:
            for consumable in self.consumable_line_ids:
                product_data.append({
                    'product_id': consumable.product_id,
                    'quantity': consumable.qty,
                    'lot_id': consumable.lot_id and consumable.lot_id.id or False,
                })
        # if not product_id:
        #     raise UserError(_("Please Configure Registration Product in Configuration first."))
        invoice = self.with_context(acs_context).acs_create_invoice(partner=self.patient_id.partner_id,
                                                                    patient=self.patient_id,
                                                                    product_data=product_data,
                                                                    inv_data={'hospital_invoice_type': 'treatment'})
        self.invoice_id = invoice.id

    def action_create_procedure_invoice(self):
        procedure_ids = self.patient_procedure_ids.filtered(lambda proc: not proc.invoice_id)
        if not procedure_ids:
            raise UserError(_("There is no Procedure to Invoice or all are already Invoiced."))

        product_data = []
        for procedure in procedure_ids:
            product_data.append({
                'product_id': procedure.product_id,
                'price_unit': procedure.price_unit,
            })

            for consumable in procedure.consumable_line_ids:
                product_data.append({
                    'product_id': consumable.product_id,
                    'quantity': consumable.qty,
                    'lot_id': consumable.lot_id and consumable.lot_id.id or False,
                })
        inv_data = {
            'physician_id': self.physician_id and self.physician_id.id or False,
        }
        invoice = self.acs_create_invoice(partner=self.patient_id.partner_id, patient=self.patient_id,
                                          product_data=product_data, inv_data=inv_data)
        procedure_ids.write({'invoice_id': invoice.id})

    def view_invoice(self):
        invoices = self.invoice_id + self.patient_procedure_ids.mapped('invoice_id')
        action = self.acs_action_view_invoice(invoices)
        action['context'].update({
            'default_partner_id': self.patient_id.partner_id.id,
            'default_patient_id': self.id,
        })
        return action

    def acs_select_treatement_for_appointment(self):
        if self._context.get('acs_current_appointment'):
            # Check if we can get back to appointment in breadcrumb.
            appointment = self.env['hms.appointment'].search(
                [('id', '=', self._context.get('acs_current_appointment'))])
            appointment.treatment_ids = [(6, 0, [self.id])]
            action = self.env["ir.actions.actions"]._for_xml_id("acs_hms.action_appointment")
            action['res_id'] = appointment.id
            action['views'] = [(self.env.ref('acs_hms.view_hms_appointment_form').id, 'form')]
            return action
        else:
            raise UserError(_("Something went wrong! Plese Open Appointment and try again"))


class TreatmentMedicineLine(models.Model):
    _name = 'treatment.medicine.line'
    _description = "Treatment Medicine Line"
    _order = "sequence"

    name = fields.Char(string='Description')
    sequence = fields.Integer("Sequence", default=10)
    product_id = fields.Many2one('product.product', ondelete="cascade", string='Medicine',
                                 domain=[('hospital_product_type', '=', 'medicament')], required=True)
    medicine_area = fields.Selection([
        ('pre-area', 'Pre-AArea'),
        ('cheek', 'Cheek'),
        ('lips', 'Lips'),
        ('chin', 'Chin'),
        ('alar', 'Alar'),
        ('marionettes', 'Marionettes'),
        ('accordion', 'Accordion lines'),
        ('forehead', 'Forehead'),
        ('peri-oral', 'Peri-Oral'),
        ('tear-trough', 'Tear-Trough'),
        ('peri-orbital', 'Peri-Orbital'),
        ('skinbooster', 'Skinbooster'),
        ('nose', 'Nose'),
        ('ear-lobe', 'Ear-lobe'),
        ('neck', 'Neck'),
        ('hands', 'Hands'),
        ('body', 'Body'),
        ('glabella', 'Glabella'),
        ('frontalis', 'Frontalis'),
        ('LCL', 'LCL'),
        ('nasalis', 'Nasalis'),
        ('LLSAN', 'LLSAN'),
        ('oris', 'O.Oris'),
        ('DAOs', 'DAOs'),
        ('mentalis', 'Mentalis'),
        ('platysma', 'Platysma'),
        ('masseters', 'Masseters'),
        ('micro-tox', 'Micro-tox'),
        ('other', 'Other'),
    ], default='pre-area', string="Area")
    amount = fields.Char(string='Amount')
    batch_number = fields.Char(string='Batch Number')
    medicine_technique = fields.Selection([
        ('bolus', 'Bolus'),
        ('micro-bolus', 'Micro-Bolus'),
        ('aliquot', 'Aliquot'),
        ('retrograde', 'Retrograde thread'),
        ('anterograde', 'Anterograde thread'),
        ('julie', 'Julie'),
        ('russian', 'Russian')], default='bolus', string='Technique')
    medicine_depth = fields.Selection([
        ('subdermal', 'Subdermal'),
        ('subcutaneous', 'Subcutaneous'),
        ('preperiosteal', 'Preperiosteal'),
        ('intramus', 'Intramuscular')], default='subdermal', string='Depth')

    medicine_method = fields.Selection([
        ('sharp', 'Sharp needle'),
        ('cannula', 'Cannula'),
        ('slip', 'Slip'),
        ('micro', 'Micro-needling'),
        ('dermal', 'Dermal puncture')], default='sharp', string='Method')

    treatment_id = fields.Many2one('hms.treatment', string='Treatment')
    company_id = fields.Many2one('res.company', ondelete="cascade", string='Clinic',
                                 related='treatment_id.company_id')

    appointment_id = fields.Many2one('hms.appointment', related='treatment_id.appointment_id', string='Appointment')
    repeat = fields.Integer(string='Repeat', default=1)
    prescription_id = fields.Many2one('prescription.order', string='Prescription')

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {'domain': {'product_id': [('hospital_product_type', '=', 'medicament')]}}
        if self.appointment_id:
            if len(self.appointment_id.prescription_line_ids) <= 0:
                result = {'domain': {
                    'product_id': [('is_required_prescription', '=', False), ('hospital_product_type', '=', 'medicament')]}}
        return result


class TreatmentTemplate(models.Model):
    _name = "treatment.template"
    _description = "Treatment Template"
    _rec_name = 'name'

    name = fields.Char(string='Title', required=True)
    notes = fields.Html(string='Treatment Note', required=True)
