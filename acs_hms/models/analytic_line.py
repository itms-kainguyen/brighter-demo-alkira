# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    description = fields.Text('Description')
    name = fields.Char('Name')
    location = fields.Selection(
        [('online', 'Online'), ('hospital', 'Hospital'), ('seminar', 'Seminar'), ('clinic', 'Clinic')],
        string='Location', default='online')

    attachment_certification_ids = fields.Many2many('ir.attachment', 'certification_attachment_rel', 'attachment_id',
                                                    'analytic_id', string='Certifications')
    certification_expiry = fields.Date('Date Expiry')

    @api.onchange('description')
    def _onchange_description(self):
        if self.description:
            self.name = self.description
