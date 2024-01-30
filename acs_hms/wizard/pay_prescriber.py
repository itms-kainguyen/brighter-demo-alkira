# coding: utf-8

from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError


class PayPrescriberWiz(models.TransientModel):
    _name = 'pay.prescriber.wiz'
    _description = "Pay Prescriber Wiz"

    payment_type = fields.Selection([
        ('outbound', 'Send'),
        ('inbound', 'Receive'),
    ], string='Payment Type', default='inbound', required=True, tracking=True)

    payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method',
                                             readonly=False, store=True, copy=False, required=True,
                                             compute='_compute_payment_method_line_id',
                                             domain="[('payment_provider_id.code', '=', 'stripe')]",
                                             help="")
    available_payment_method_line_ids = fields.Many2many('account.payment.method.line',
                                                         compute='_compute_payment_method_line_fields')
    payment_method_id = fields.Many2one(
        related='payment_method_line_id.payment_method_id',
        string="Method",
        tracking=True,
        store=True
    )
    partner_id = fields.Many2one('res.partner', 'Partner', default=lambda self: self.env.user.partner_id)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    payment_token_id = fields.Many2one(
        string="Select Credit Card", comodel_name='payment.token',
        domain="""[
                ('company_id', '=', company_id),
                ('provider_id.capture_manually', '=', False),
                ('partner_id', '=', partner_id)
         ]""",
        help="Note that only tokens from providers allowing to capture the amount are available.")
    # domain="""[
    #                 ('id', 'in', suitable_payment_token_ids),
    #             ]""",
    suitable_payment_token_ids = fields.Many2many(
        comodel_name='payment.token',
        compute='_compute_suitable_payment_token_ids', precompute=True,
        compute_sudo=True,
    )
    prescriber_fee = fields.Float('Prescriber fee', default=25.0)

    payment_transaction_id = fields.Many2one(
        string="Payment Transaction",
        comodel_name='payment.transaction',
        readonly=True,
        auto_join=True,  # No access rule bypass since access to payments means access to txs too
    )

    payment_icon_ids = fields.Many2many(
        string="Supported Payment Icons", comodel_name='payment.icon', compute='_compute_payment_icon_ids', )

    @api.model
    def default_get(self, fields):
        res = super(PayPrescriberWiz, self).default_get(fields)
        res_ids = self._context.get('active_ids')
        prescription = self.env['prescription.order'].browse(res_ids)
        res.update({
            'prescriber_fee': prescription.prescriber_fee
        })
        return res

    def _compute_suitable_payment_token_ids(self):
        active_id = self.env.context.get('active_id')
        current_id = self.env['prescription.order'].browse(active_id)
        for payment in self:
            related_partner_ids = (
                    self.env.user.partner_id
                    | self.env.user.partner_id.commercial_partner_id
                    | self.env.user.partner_id.commercial_partner_id.child_ids
            )._origin
            payment.suitable_payment_token_ids = self.env['payment.token'].sudo().search([
                ('company_id', '=', payment.company_id.id),
                ('provider_id.capture_manually', '=', False),
                ('partner_id', 'in', related_partner_ids.ids),
                ('provider_id', '=', payment.payment_method_line_id.payment_provider_id.id),
            ])

    @api.depends('available_payment_method_line_ids')
    def _compute_payment_method_line_id(self):
        for pay in self:
            available_payment_method_lines = pay.available_payment_method_line_ids

            # Select the first available one by default.
            if pay.payment_method_line_id in available_payment_method_lines:
                if pay.payment_method_line_id.code == 'stripe':
                    pay.payment_method_line_id = pay.payment_method_line_id
            elif available_payment_method_lines:
                for line in available_payment_method_lines:
                    if line.code == 'stripe':
                        pay.payment_method_line_id = line._origin
            else:
                pay.payment_method_line_id = False

    @api.depends('payment_type')
    def _compute_payment_method_line_fields(self):
        for pay in self:
            journal = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)
            if journal:
                pay.available_payment_method_line_ids = journal._get_available_payment_method_lines(pay.payment_type)

    @api.depends('payment_method_line_id')
    def _compute_payment_icon_ids(self):
        for pay in self:
            if pay.payment_method_line_id:
                pay.payment_icon_ids = pay.payment_method_line_id.payment_provider_id.payment_icon_ids

    def pay_prescription(self):
        active_id = self.env.context.get('active_id')
        current_id = self.env['prescription.order'].browse(active_id)
        if not self.payment_token_id:
            raise ValidationError(_('Please Select Credit Card.'))
        current_id.button_confirm()
        journal = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)
        transaction = self.env['account.payment'].sudo().create({
            'payment_type': self.payment_type,
            'amount': self.prescriber_fee,
            'journal_id': journal.id if journal else False,
            'payment_method_line_id': self.payment_method_line_id.id,
            'payment_token_id': self.payment_token_id.id,
            'use_electronic_payment_method': True,
            'partner_id': self.partner_id.id,
            'ref': current_id.name,
            'is_internal_transfer': False,
        })
        if transaction:
            transaction.action_post()
            self.payment_transaction_id = transaction.payment_transaction_id.id
            config_parameter_obj = self.env['ir.config_parameter'].sudo()
            url = config_parameter_obj.get_param('web.base.url')
            url += '/web#id={id}&cids=1&model=prescription.order&view_type=form'.format(id=current_id.id)
            body_html = '''<div style="padding:0px;margin:auto;background: #FFFFFF repeat top /100%;color:#777777">
                            <p>Hi <strong>{prescriber}</strong>,</p>
                            <p>This is <strong>{nurse}</strong>, a nurse at <strong>{clinic}</strong>, reaching out regarding a current patient under our care.</p>
                            <p>Patient Details:</p>
                            <p>Name: <strong>{patient}</strong></p>
                            <p>Prescription Order: <a href="{link}">{order}</a></p>
                            <p>Current Situation: The patient is here for their scheduled appointment and has been evaluated. Based on their condition and our preliminary assessment, we believe that a prescription for [Medicines Name] would be beneficial for their treatment plan.<p>
                            <br/>
                            <p>Action Required:</p>
                            <p>We request your expertise to review & authorize the necessary prescription. We plan to initiate a telehealth call shortly to discuss this case in more detail.</p>
                            <br/>
                            <p>Patient Background:</p>
                            <p>The patient has completed a medical checklist and their allergies are: [Allergies]. We are ready to provide any additional information required during the telehealth call.</p>
                            <br/><br/>
                            Thank you
                       </div>
                       '''.format(prescriber=current_id.physician_id.name, nurse=current_id.nurse_id.name, clinic=current_id.department_id.name, patient=current_id.patient_id.name,
                                  link=url, order=current_id.name)
            channel = self.env['mail.channel'].channel_get([current_id.physician_id.partner_id.id])
            channel_id = self.env['mail.channel'].browse(channel["id"])
            channel_id.message_post(
                body=(body_html),
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
            )
            channel_prescriber_id = self.env['mail.channel'].browse(37)
            if channel_prescriber_id:
                channel_prescriber_id.message_post(
                    body=(body_html),
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                )

    def save_payment(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': '/my/payment_method',
        }
