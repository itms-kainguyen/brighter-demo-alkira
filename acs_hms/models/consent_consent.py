from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Consent(models.Model):
    _inherit = 'consent.consent'

    appointment_id = fields.Many2one('hms.appointment', string='Appointment', required=1)

    def action_open_form(self):
        # return the form view of this partner
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "consent.consent",
            "res_id": self.id,
            "view_mode": "form",
            "view_type": "form",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
        }
    
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('consent.consent') or 'Consent'
            vals['content'] = None
            if vals.get('category_id'):
                category_consent = self.env['document.page'].browse(vals['category_id'])
                vals['content'] = category_consent.content
                vals['patient_signature'] = None
                vals['patient_signed_by'] = None

        return super(Consent, self).create(vals_list)

    def write(self, vals):
        if vals.get('category_id'):
            category_consent = self.env['document.page'].browse(vals['category_id'])
            vals['content'] = category_consent.content
            vals['patient_signature'] = None
            vals['patient_signed_by'] = None

        return super(Consent, self).write(vals)

    def consent_forms_confirm(self):
        # return the form view of this partner
        self.ensure_one()
        template_consent = self.env.ref('acs_hms.consent_appointment_form_email')
        hms_appointment_object = self.env['hms.appointment'].browse(self.appointment_id.id)
        for itms_consent_id in hms_appointment_object.consent_ids:
            # Generate the PDF attachment.
            if itms_consent_id.id == self.id:
                pdf_content, dummy = self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                    'itms_consent_form.report_consent', res_ids=[itms_consent_id.id])
                attachment = self.env['ir.attachment'].create({
                    'name': itms_consent_id.name,
                    'type': 'binary',
                    'raw': pdf_content,
                    'res_model': itms_consent_id._name,
                    'res_id': itms_consent_id.id
                })
                # Add the attachment to the mail template.
                template_consent.attachment_ids += attachment
                email_values = {'itms_consent_id': itms_consent_id}
        # Send the email.
        template_consent_creation = template_consent.with_context(**email_values).sudo().send_mail(
            self.appointment_id.id, raise_exception=False, force_send=True)

        if template_consent_creation:
            return True
        else:
            raise UserError(_("Error: Send email."))