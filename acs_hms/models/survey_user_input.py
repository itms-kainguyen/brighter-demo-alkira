# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    appointment_id = fields.Many2one('hms.appointment', string='Appointment')

    @api.model_create_multi
    def create(self, values_list):
        return super().create(values_list)


class AppointmentIndividualSurveyAnswer(models.Model):
    _name = "appointment.individual.survey.answer"
    _description = "Individual"

    appointment_id = fields.Many2one('hms.appointment', string='Appointment')
    name = fields.Char('Question')
    answer = fields.Char('Answer')
    date = fields.Datetime()


class AppointmentRelevantSurveyAnswer(models.Model):
    _name = "appointment.relevant.survey.answer"
    _description = "Relevant"

    appointment_id = fields.Many2one('hms.appointment', string='Appointment')
    name = fields.Char('Question')
    answer = fields.Char('Answer')
    date = fields.Datetime()


class AppointmentMedicationSurveyAnswer(models.Model):
    _name = "appointment.medication.survey.answer"
    _description = "Medication"

    appointment_id = fields.Many2one('hms.appointment', string='Appointment')
    name = fields.Char('Question')
    answer = fields.Char('Answer')
    date = fields.Datetime()


class AppointmentAdditionSurveyAnswer(models.Model):
    _name = "appointment.addition.survey.answer"
    _description = "Additional"

    appointment_id = fields.Many2one('hms.appointment', string='Appointment')
    name = fields.Char('Question')
    answer = fields.Char('Answer')
    date = fields.Datetime()
