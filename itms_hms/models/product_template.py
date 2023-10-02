# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    retail_price = fields.Float(string='RRP Price', digits='Product Unit of Measure')
    hospital_product_type = fields.Selection(
        selection_add=[('shop', 'Shop'), ('pos', 'POS'), ('course', 'eLearning'), ('services', 'Services')])


class ProductProduct(models.Model):
    _inherit = 'product.product'

    retail_price = fields.Float(string='RRP Price', digits='Product Unit of Measure')
