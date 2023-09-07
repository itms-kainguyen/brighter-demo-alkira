# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    retail_price = fields.Float(string='RRP Price', digits='Product Unit of Measure')
    brand = fields.Char('Brand')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    retail_price = fields.Float(string='RRP Price', digits='Product Unit of Measure')
    brand = fields.Char('Brand')
