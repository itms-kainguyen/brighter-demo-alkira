# coding: utf-8

from odoo import models, api, fields

class AcsPainLevel(models.TransientModel):
    _name = 'hms.isdone'
    _description = "Process Done"

    name = fields.Char()