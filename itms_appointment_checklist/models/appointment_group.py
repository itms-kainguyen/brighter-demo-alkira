# coding: utf-8

from odoo import fields, models


class appointment_group(models.Model):
    _name = 'appointment.group'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Group Name')
    member_ids = fields.Many2many(
        'res.users', string='Users',
        domain="[('share', '=', False)]", search='_search_member_ids',
        help="Users assigned to this group.")
    check_line_ids = fields.One2many(
        "appointment.check.item",
        "group_id",
        string="Check Lists",
        copy=True,
    )
    no_stages_ids = fields.One2many(
        "appointment.check.item",
        "group_no_id",
        string="""Determine the states, the transfer to which does not require filling in the check lists at the current
        stage""",
        copy=True,
    )
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    active = fields.Boolean(string="Active", default=True, index=True)
