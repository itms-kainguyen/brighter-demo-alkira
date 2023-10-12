# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

states = [('draft', 'Draft'), ('approved', 'Validated')]

class LetterTags(models.Model):
    _name = 'letter.tags'

    name = fields.Char('Name')

class kmSystem(models.Model):
    _name = 'km.system'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Knowledge Base'

    name = fields.Char('Title', readonly=True, states={'draft': [('readonly', False)]}, required=True)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(states, string='Status', readonly=True, default='draft', track_visibility='onchange')
    content = fields.Html('Content', states={'draft': [('readonly', False)]})
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, states={'draft': [('readonly', False)]})
    description = fields.Text('Reference', states={'draft': [('readonly', False)]})
    date = fields.Date('Date', states={'draft': [('readonly', False)]})
    tags = fields.Many2many('letter.tags', 'letter_tag_knowledge_rel','knowledge_id','tag_id', string='Tags')

    def approve_action(self):
        self.write({'state':'approved'})