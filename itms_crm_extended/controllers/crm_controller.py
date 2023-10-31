from odoo import http, SUPERUSER_ID, _, api
from odoo.addons.website_crm.controllers.website_form import WebsiteForm
from odoo.addons.website.controllers.form import WebsiteForm as WebsiteForm2
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.http import request
from odoo.exceptions import UserError
import re


def extract_values(text, patterns):
    results = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            results[field] = match.group(1)
        else:
            results[field] = None
    return results


# Define regular expression patterns to capture the values
patterns = {
    'entity_type': r'entity_type : (.+)',
    'trading_name': r'trading_name : (.+)',
    'abn':  r'abn : (.+)',
    'company_registered_address': r'company_registered_address : (.+)',
    'company_website': r'company_website : (.+)',
    'company_instagram_handle': r'company_instagram_handle : (.+)',
    'delivery_hours_1': r'delivery_hours_1 : (.+)',
    'delivery_hours_2': r'delivery_hours_2 : (.+)',
    'delivery_hours_3': r'delivery_hours_3 : (.+)',
    'delivery_hours_4': r'delivery_hours_4 : (.+)',
    'delivery_hours_5': r'delivery_hours_5 : (.+)',
    'delivery_hours_6': r'delivery_hours_6 : (.+)',
    'delivery_hours_7': r'delivery_hours_7 : (.+)',
    'best_contact_number': r'best_contact_number : (.+)',
    'best_contact_email': r'best_contact_email : (.+)',
    'practitioner_name': r'practitioner_name : (.+)',
    'healthcare_qualifications': r'healthcare_qualifications : (.+)',
    'ahpra_details': r'ahpra_details : (.+)',
    'owner_employee': r'owner_employee : (.+)',
    'insurance': r'insurance : (.+)',
    'key_practitioner_years_of_practice': r'key_practitioner_years_of_practice : (.+)',
    'scope_of_practice': r'scope_of_practice : (.+)',
    'current_prescribing_service': r'current_prescribing_service : (.+)',
    'current_authorising_practitioner_name': r'current_authorising_practitioner_name : (.+)',
    'authorising_practice_clinic_name': r'authorising_practice_clinic_name : (.+)',
    'current_scheduled_product_accounts': r'current_scheduled_product_accounts : (.+)',
    'estimated_annual_scheduled_product_purchase_value': r'estimated_annual_scheduled_product_purchase_value : (.+)',

}


class EnquiryRegistrationForm(WebsiteForm):
    def insert_record(self, request, model, values, custom, meta=None):
        lead_id = super(EnquiryRegistrationForm, self).insert_record(request, model, values, custom, meta=None)
        if model.model == 'crm.lead':
            cutstom_values = extract_values(custom, patterns)
            print(values)
            print(cutstom_values)
             #raise UserError(f"{custom} {cutstom_values} {request} {self} {values}")

            base_url = http.request.env['ir.config_parameter'].get_param('web.base.url')
            action_id = request.env.ref('crm.crm_lead_all_leads', raise_if_not_found=False)
            crm_url = f'{base_url}/web#id={lead_id}&model=crm.lead&view_type=form&action={action_id.id}'
            print(crm_url)
            lead = request.env['crm.lead'].browse(lead_id)
            if cutstom_values:
                lead.write({
                    'entity_type': cutstom_values['entity_type'],
                    'trading_name': cutstom_values['trading_name'],
                    'abn': cutstom_values['abn'],
                    'company_registered_address': cutstom_values['company_registered_address'],
                    'company_website': cutstom_values['company_website'],
                    'company_instagram_handle': cutstom_values['company_instagram_handle'],
                    'delivery_hours_1': cutstom_values['delivery_hours_1'],
                    'delivery_hours_2': cutstom_values['delivery_hours_2'],
                    'delivery_hours_3': cutstom_values['delivery_hours_3'],
                    'delivery_hours_4': cutstom_values['delivery_hours_4'],
                    'delivery_hours_5': cutstom_values['delivery_hours_5'],
                    'delivery_hours_6': cutstom_values['delivery_hours_6'],
                    'delivery_hours_7': cutstom_values['delivery_hours_7'],
                    'best_contact_number': cutstom_values['best_contact_number'],
                    'mobile': cutstom_values['best_contact_number'],
                    'best_contact_email': cutstom_values['best_contact_email'],
                    'practitioner_name': cutstom_values['practitioner_name'],
                    'healthcare_qualifications': cutstom_values['healthcare_qualifications'],
                    'ahpra_details': cutstom_values['ahpra_details'],
                    'owner_employee': cutstom_values['owner_employee'],
                    'insurance': cutstom_values['insurance'],
                    'key_practitioner_years_of_practice': cutstom_values['key_practitioner_years_of_practice'],
                    'scope_of_practice': cutstom_values['scope_of_practice'],
                    'current_prescribing_service': cutstom_values['current_prescribing_service'],
                    'current_authorising_practitioner_name': cutstom_values['current_authorising_practitioner_name'],
                    'authorising_practice_clinic_name': cutstom_values['authorising_practice_clinic_name'],
                    'current_scheduled_product_accounts': cutstom_values['current_scheduled_product_accounts'],
                    'estimated_annual_scheduled_product_purchase_value': cutstom_values['estimated_annual_scheduled_product_purchase_value'],
                })
        return lead_id
