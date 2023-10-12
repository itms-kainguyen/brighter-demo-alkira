# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class AfterCare(models.Model):
    _inherit = 'patient.aftercare'

    appointment_id = fields.Many2one('hms.appointment', string='Appointment')

    @api.onchange('category_id')
    def onchange_category_id(self):
        self.ensure_one()
        if self.category_id:
            self.name = self.category_id.title

    def action_open_form(self):
        # return the form view of this partner
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "patient.aftercare",
            "res_id": self.id,
            "view_mode": "form",
            "view_type": "form",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
        }
