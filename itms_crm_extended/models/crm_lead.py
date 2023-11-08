from odoo import fields, models, api


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    entity_type = fields.Char()
    # entity_type = fields.Selection([
    #     ('Pty Ltd Company', 'Pty Ltd Company'),
    #     ('Sole Trader', 'Sole Trader'),
    #     ('Partnership', 'Partnership'),
    #     ('Trustee', 'Trustee'),
    # ], string='Entity Type', multiple=True)
    trading_name = fields.Char()
    abn = fields.Char('Company ABN')
    company_registered_address = fields.Char()
    company_website = fields.Char()
    company_instagram_handle = fields.Char()
    delivery_hours_1 = fields.Char('Monday')
    delivery_hours_2 = fields.Char('Tuesday')
    delivery_hours_3 = fields.Char('Wednesday')
    delivery_hours_4 = fields.Char('Thursday')
    delivery_hours_5 = fields.Char('Friday')
    delivery_hours_6 = fields.Char('Saturday')
    delivery_hours_7 = fields.Char('Sunday')
    best_contact_number = fields.Char()
    best_contact_email = fields.Char()
    practitioner_name = fields.Char()
    healthcare_qualifications = fields.Selection([
        ('Registered Nurse', 'Registered Nurse'),
        ('Nurse Practitioner', 'Nurse Practitioner'),
        ('Medical Practitioner', 'Medical Practitioner'),
    ], string='Healthcare Qualifications')
    ahpra_details = fields.Char('AHPRA Details')
    owner_employee = fields.Char('Owner/Employee')
    insurance = fields.Char()
    key_practitioner_years_of_practice = fields.Selection([
        ('12month', '< 12months'),
        ('1_2year', '1-2 years'),
        ('2_5year', '2-5 years'),
        ('5_7year', '5-7 years'),
        ('7_10year', '7-10 years'),
        ('10year_plus', 'Over 10 years'),
    ], string='Key Practitioner Years of Practice')
    scope_of_practice = fields.Char()
    current_prescribing_service = fields.Selection([
        ('Fresh Clinics', 'Fresh Clinics'),
        ('Instantscripts', 'Instantscripts'),
        ('APA', 'APA'),
        ('Ageless', 'Ageless'),
        ('Other – please list', 'Other – please list'),
    ], string='Current Prescribing Service')
    current_authorising_practitioner_name = fields.Char()
    authorising_practice_clinic_name = fields.Char()
    current_scheduled_product_accounts = fields.Selection([
        ('Galderma', 'Galderma'),
        ('Allergan', 'Allergan'),
        ('Teoxane', 'Teoxane'),
        ('Hugel', 'Hugel'),
        ('Merz', 'Merz'),
        ('Envogue', 'Envogue'),
        ('Avaderm Australia', 'Avaderm Australia'),
        ('Cryomed', 'Cryomed'),
        ('Dermocosmètica', 'Dermocosmètica'),
        ('Austramedix', 'Austramedix'),
        ('Aqualift', 'Aqualift'),
        ('Other – please list', 'Other – please list'),
    ], string='Current Scheduled Product Accounts')
    estimated_annual_scheduled_product_purchase_value = fields.Selection([
        ('10_50k', '$10-50k'),
        ('50_100k', '$50-100K'),
        ('100_150k', '$100-150K'),
        ('150_200k', '$150-200k'),
        ('200_300k', '$200-300k'),
        ('300_400k', '$300-400k'),
        ('400_500k', '$400-500k'),
        ('500k_plus', '>$500k'),
    ], string='Estimated Annual Scheduled Product Purchase value')

    def action_create_subscription(self):
        # creating a subscription order based on selected lead (state=opportunity)
        print('Creating Subscription')
        return {
            'name': 'Create New Subscription',
            'type': 'ir.actions.act_window',
            'res_model': 'subscription.package',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('itms_crm_extended.view_subscription_package_popup').id,
            'context': {'default_lead': self.id}
        }


class SubscriptionPackageInherit(models.Model):
    _inherit = "subscription.package"

    lead = fields.Many2one('crm.lead', string='Opportunity')

    @api.depends('reference_code')
    def _compute_name(self):
        """It displays record name as combination of short code, reference
        code and partner name """
        for rec in self:
            plan_id = self.env['subscription.package.plan'].search(
                [('id', '=', rec.plan_id.id)])
            if plan_id.short_code and rec.reference_code:
                print(rec.lead.partner_id)
                print(rec.lead.name)
                if rec.partner_id:
                    rec.name = plan_id.short_code + '/' + rec.reference_code + '-' + rec.partner_id.name
                else:
                    print(rec.lead.partner_id)
                    print(rec.lead.name)
                    rec_name = rec.lead.partner_id.name or rec.lead.name
                    rec.partner_id = rec.lead.partner_id
                    rec.name = plan_id.short_code + '/' + rec.reference_code + '-' + str(rec_name)

    def action_save_subscription(self):
        print('action_save_subscription')
        self.ensure_one()
        # new_record = self.create({
        #     'name': self.name,
        #     'parent_id': self.parent_id.id
        # })
        # crm_lead = self.env["crm.lead"].browse(self)
        if self.lead:
            self.lead.message_post(
                body="Subscription Package created '%s' has been created." % self.name,
                subject="Subscription Package created",
                # subtype_id='mail.mt_comment',
            )
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'subscription.package',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.id,
        }
        return action



