# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, models

class Product(models.Model):
    _inherit = "product.product"

    def _get_domain_locations(self):
        location = self.env.context.get('location')
        #location now have to consider the user department location
        if location:
            return super(Product, self)._get_domain_locations()
        location = self.env.user.department_ids.mapped('location_id')
        if location:
            # put the location in the context
            self.env.context = dict(self.env.context, location=location.id)
        return super(Product, self)._get_domain_locations()
