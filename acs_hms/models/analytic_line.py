# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    name = fields.Text('Description', required=True)
    location = fields.Selection(
        [('online', 'Online'), ('hospital', 'Hospital'), ('seminar', 'Seminar'), ('clinic', 'Clinic')],
        string='Location', default='online')

    attachment_certification_ids = fields.Many2many('ir.attachment', 'certification_attachment_rel', 'attachment_id',
                                                    'analytic_id', string='Certifications')
    certification_expiry = fields.Date('Date Expiry')
