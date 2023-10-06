# coding: utf-8

from odoo import fields, models


class AppointmentChecklistHistory(models.Model):
    """
    A model to keep each change of check list per sale order
    """
    _name = "appointment.checklist.history"
    _description = "Check List History"
    _order = "complete_date DESC,id"

    check_list_id = fields.Many2one("appointment.check.item", string="Check Item", )
    appointment_id = fields.Many2one("hms.appointment")
    complete_date = fields.Datetime(string="Date", default=lambda self: fields.Datetime.now(), )
    user_id = fields.Many2one(
        "res.users",
        "User",
        default=lambda self: self.env.user.id,
    )
    done_action = fields.Selection(
        [("done", "Complete"), ("reset", "Reset")],
        string="Action",
        default="done",
    )
