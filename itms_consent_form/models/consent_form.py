# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class Consent(models.Model):
    _name = 'consent.consent'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Patient Consent Form"

    name = fields.Char('Name', required=True, index='trigram')
    content = fields.Html('Content')
    patient_id = fields.Many2one('hms.patient', string='Patient')
    category_id = fields.Many2one('document.page', domain=[('type', '=', 'category')], string='Category')
    nurse_id = fields.Many2one('res.users', domain=[('physician_id', '=', False)], readonly=1, string='Nurse',
                               default=lambda self: self.env.user.id)
    patient_attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'consent.form')],
                                             string='Patient Attachments')
    nurse_attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'consent.form')],
                                           string='Nurse Attachments')
    patient_signature = fields.Binary(string="Patient Signature")
    patient_signed_by = fields.Char(
        string="Patient Signed By", copy=False)
    patient_signed_on = fields.Datetime(
        string="Patient Signed On", copy=False)
    is_agree = fields.Boolean('I read and give my consent to this document')
    nurse_signature = fields.Binary(string="Nurse Signature", copy=False)
    nurse_signed_by = fields.Char(compute='_compute_nurse_signature', string="Nurse Signed By", readonly=1, copy=False,
                                  store=True)
    nurse_signed_on = fields.Datetime(compute='_compute_nurse_signature',
                                      string="Nurse Signed On", readonly=1, copy=False)
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company, store=True)

    @api.depends('nurse_id', 'nurse_signature')
    def _compute_nurse_signature(self):
        for rec in self:
            rec.nurse_signed_by = None
            rec.nurse_signed_on = None
            if rec.nurse_signature and rec.nurse_id:
                rec.nurse_signed_by = rec.nurse_id.name
                rec.nurse_signed_on = datetime.datetime.now()

    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('itms_consent_form.action_consent_form')

    @api.onchange('category_id')
    def onchange_category_id(self):
        self.content = None
        if self.category_id:
            self.content = self.category_id.template
            self.patient_signature = None
            self.patient_signed_by = None
            self.nurse_signature = None
            self.nurse_signed_by = None

    def _compute_access_url(self):
        super()._compute_access_url()
        for order in self:
            order.access_url = f'/my/consent-form/{order.id}'

    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s' % self.category_id.name

    def action_preview_consent(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }

    def action_consent_send(self):
        self.ensure_one()
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        email_to = self.patient_id.email
        ctx = {
            'default_model': 'consent.consent',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'email_to': email_to or False,
            'sign_url': self.get_portal_url(),
            'patient_name': self.patient_id.name,
            # 'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def _find_mail_template(self):
        self.ensure_one()
        return self.env.ref('itms_consent_form.email_patient_consent_form', raise_if_not_found=False)


class Partner(models.Model):
    _inherit = 'res.partner'

    # consent_count = fields.Integer(compute='_compute_consent_count', string='Consent Count')
    # consent_ids = fields.One2many('consent.consent', 'patient_id', 'Consent Form')
    #
    # def _compute_consent_count(self):
    #     consents = self.env['consent.consent']._read_group([
    #         ('patient_id', 'in', self.ids)
    #     ], fields=['patient_id'], groupby=['patient_id'], lazy=False)
    #     mapping = {(consent['patient_id'][0]): consent['__count'] for consent in consents}
    #     for rule in self:
    #         rule.consent_count = mapping.get(rule.id, 0)
    #
    # def action_view_consent_form(self):
    #     action = self.env['ir.actions.act_window']._for_xml_id('itms_consent_form.act_res_partner_2_consent')
    #     all_child = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
    #     action["domain"] = [("patient_id", "in", all_child.ids)]
    #     return action


class ACSPatient(models.Model):
    _inherit = 'hms.patient'

    consent_count = fields.Integer(compute='_compute_consent_count', string='Consent Count')
    consent_ids = fields.One2many('consent.consent', 'patient_id', 'Consent Form')

    def _compute_consent_count(self):
        consents = self.env['consent.consent']._read_group([
            ('patient_id', 'in', self.ids)
        ], fields=['patient_id'], groupby=['patient_id'], lazy=False)
        mapping = {(consent['patient_id'][0]): consent['__count'] for consent in consents}
        for rule in self:
            rule.consent_count = mapping.get(rule.id, 0)

    def action_view_consent_form(self):
        action = self.env['ir.actions.act_window']._for_xml_id('itms_consent_form.act_res_partner_2_consent')
        all_child = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        action["domain"] = [("patient_id", "in", all_child.ids)]
        return action
