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

