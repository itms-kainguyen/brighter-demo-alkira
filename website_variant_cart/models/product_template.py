# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2016-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# License URL :<https://store.webkul.com/license.html/>
##########################################################################
from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hide_var_list_view = fields.Boolean("Hide Variants List View",help="Hide product variants list view(multi-variants view for add to cart) on product page")

    def get_product_possible_variants(self):
        self.ensure_one()
        possible_variants = self.env["product.product"]
        for product in self.product_variant_ids:
            if self._is_combination_possible(combination=product.product_template_attribute_value_ids):
                possible_variants += product
        return possible_variants

    def has_dynamic_or_never_attributes(self):
        self.ensure_one()
        return any(a.create_variant in ['dynamic','no_variant'] for a in self.valid_product_template_attribute_line_ids.attribute_id)