# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_default_contact_global = fields.Boolean(
        "Default Contact Global?", 
        config_parameter="itms_base_multi_company.is_default_contact_global"
    )
    is_default_product_global = fields.Boolean(
        "Default Product Global?", 
        config_parameter="itms_base_multi_company.is_default_product_global"
    )