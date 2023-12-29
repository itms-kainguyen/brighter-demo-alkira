from odoo import models, fields, api

class TreatmentProcedure(models.Model):
    _name = 'treatment.procedure'
    _description = 'Treatment Procedure'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    category_ids = fields.Many2many(
        'document.page', 
        string='Consent Forms', 
        domain=[('type', '=', 'content'), ('parent_id.name', '=', 'Consent')])
