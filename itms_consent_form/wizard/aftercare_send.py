# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.mail.wizard.mail_compose_message import _reopen
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang


class AftercareSend(models.TransientModel):
    _name = 'patient.aftercare.send'
    _inherits = {'mail.compose.message': 'composer_id'}
    _description = 'Aftercare Send'

    patient_aftercare_ids = fields.Many2many('hms.patient', 'patient_aftercare_sendemail_rel', 'patient_id',
                                             'aftercare_send_id',
                                             string='Patients')
    composer_id = fields.Many2one('mail.compose.message', string='Composer', required=True, ondelete='cascade')
    template_id = fields.Many2one(
        'mail.template', 'Use template',
        domain="[('model', '=', 'patient.aftercare.send')]"
    )
    aftercare_id = fields.Many2one('patient.aftercare', string="AfterCare", ondelete='cascade')

    @api.model
    def default_get(self, fields):
        res = super(AftercareSend, self).default_get(fields)
        res_ids = self._context.get('active_ids')
        cares = self.env['patient.aftercare'].browse(res_ids)
        if not cares:
            raise UserError(_("You can only send cares."))

        composer = self.env['mail.compose.message'].create({
            'composition_mode': 'mass_mail'  # if len(res_ids) == 1 else 'mass_mail',
        })
        res.update({
            # 'patient_aftercare_ids': res_ids,
            'composer_id': composer.id,
        })
        return res

    # @api.onchange('recipient_ids')
    # def _onchange_recipient_ids(self):
    #     for wizard in self:
    #         wizard.email_to = ','.join(str([partner.email for partner in wizard.recipient_ids]))

    @api.onchange('patient_aftercare_ids')
    def _compute_composition_mode(self):
        for wizard in self:
            wizard.composer_id.composition_mode = 'mass_mail'

    @api.onchange('template_id')
    def onchange_template_id(self):
        for wizard in self:
            if wizard.composer_id:
                wizard.composer_id.template_id = wizard.template_id.id
                wizard._compute_composition_mode()
                wizard.composer_id._onchange_template_id_wrapper()

    def _send_email(self):
        self.composer_id.with_context(mail_notify_author=self.env.user.partner_id in self.composer_id.partner_ids,
                                      mailing_document_based=True
                                      )._action_send_mail()

    def send_action(self):
        self.ensure_one()
        # active_ids = self.env.context.get('active_ids', self.res_id)
        # active_records = self.env[self.model].browse(active_ids)
        # # langs = active_records.mapped('partner_id.lang')
        # default_lang = get_lang(self.env)
        # for lang in ([default_lang]):
        #     self_lang = self.with_context(active_ids=active_records, lang=lang)
        #     self_lang.onchange_template_id()
        self._send_email()
        return {'type': 'ir.actions.act_window_close'}

    def save_as_template(self):
        self.ensure_one()
        self.composer_id.action_save_as_template()
        self.template_id = self.composer_id.template_id.id
        action = _reopen(self, self.id, self.model, context=self._context)
        action.update({'name': _('Send Aftercare')})
        return action
