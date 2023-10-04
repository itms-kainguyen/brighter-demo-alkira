# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


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
        # mail_template = self.env.ref('itms_consent_form.email_patient_aftercare_form', raise_if_not_found=False)
        # if mail_template and mail_template.lang:
        #      lang = mail_template._render_lang(self.ids)[self.id]
        email_to = False
        mail_template = None
        ctx = {
            'default_aftercare_id': self.id,
            'default_name': self.name,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'mass_mail',
            'email_to': email_to or False,
            'force_email': True,
            'default_attachment_ids': [(6, 0, self.attachment_ids.ids)]
        }
        return {
            'name': 'Send email',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'patient.aftercare.send',
            'views': [(False, 'form')],
            'view_id': self.env.ref('itms_consent_form.patient_aftercare_send_view_form').id,
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

    # aftercare_ids = fields.One2many('patient.aftercare.send', 'patient_id', 'Aftercare')

    def action_view_aftercare(self):
        ctx = {}
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'patient.aftercare',
            'views': [(False, 'tree'), (False, 'form')],
            'view_id': self.env.ref('itms_consent_form.view_aftercare_tree').id,
            'target': 'new',
            'context': ctx,
        }
