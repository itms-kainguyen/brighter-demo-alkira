# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _, Command


class AfterCare(models.Model):
    _name = 'patient.aftercare'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Patient Aftercare"

    name = fields.Char('Title', required=1)
    content = fields.Html('Content')
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'patient.aftercare')],
                                     string='Attachments')
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company, store=True)

    def action_aftercare_send(self):
        self.ensure_one()
        lang = self.env.context.get('lang')
        mail_template = self.env.ref('itms_consent_form.appointment_patient_aftercare_form', raise_if_not_found=False)
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        email_to = False
        compose_form = self.env.ref('itms_consent_form.patient_aftercare_send_view_form', raise_if_not_found=False)
        partner_ids = []
        if self._context.get('partner_id'):
            partner_ids = self.env['res.partner'].search([('id', '=', self._context.get('partner_id'))])
        appointment = False
        if self._context.get('appointment_id'):
            appointment = self.env['hms.appointment'].search([('id', '=', self._context.get('appointment_id'))])

        ctx = {
            'default_aftercare_id': self.id,
            'default_appointment_id': appointment.id if appointment else False,
            'default_subject': self.name,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'mass_mail',
            'force_email': True,
            'default_attachment_ids': self.attachment_ids.ids,
            'default_partner_ids': partner_ids.ids if len(partner_ids) > 0 else [],
            'active_ids': self.ids
        }
        return {
            'name': _('Send email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'patient.aftercare.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def action_aftercare_download(self):
        for attach in self.attachment_ids:
            action = {
                'type': 'ir.actions.act_url',
                'url': 'web/content/?model=ir.attachment&download=true&id=%s' % (attach.id),
                'target': 'new', }
            return action


class ACSPatient(models.Model):
    _inherit = 'hms.patient'

    aftercare_history_ids = fields.One2many('patient.aftercare.history', 'patient_id', 'Aftercare')

    def action_view_aftercare(self):
        ctx = {'partner_id': self.partner_id.id}
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'patient.aftercare',
            'views': [(False, 'tree'), (False, 'form')],
            'view_id': self.env.ref('itms_consent_form.view_aftercare_tree').id,
            'target': 'new',
            'context': ctx,
        }


class AfterCareHistory(models.Model):
    _name = 'patient.aftercare.history'
    _description = "Patient Aftercare History"

    name = fields.Char('Title')
    aftercare_id = fields.Many2one('patient.aftercare', string="AfterCare", ondelete='cascade')
    patient_id = fields.Many2one('hms.patient', string="Patient", ondelete='cascade')
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'patient.aftercare')],
                                     string='Attachments')
    state = fields.Selection([('sent', 'Sent'), ('fail', 'Delivery Failed')], string='Email Status')
    date = fields.Datetime('Date')
    user_id = fields.Many2one('res.users', 'By')
    appointment_id = fields.Many2one("hms.appointment", string="Appointment")
