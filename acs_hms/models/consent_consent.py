from odoo import models, fields, api


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
                vals['content'] = category_consent.template
                vals['patient_signature'] = None
                vals['patient_signed_by'] = None

        return super(Consent, self).create(vals_list)

    def write(self, vals):
        if vals.get('category_id'):
            category_consent = self.env['document.page'].browse(vals['category_id'])
            vals['content'] = category_consent.template
            vals['patient_signature'] = None
            vals['patient_signed_by'] = None

        return super(Consent, self).write(vals)