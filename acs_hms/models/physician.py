# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)
from odoo import exceptions


class Physician(models.Model):
    _inherit = 'hms.physician'

    def _phy_rec_count(self):
        Treatment = self.env['hms.treatment']
        Appointment = self.env['hms.appointment']
        Prescription = self.env['prescription.order']
        Patient = self.env['hms.patient']
        for record in self.with_context(active_test=False):
            record.treatment_count = Treatment.search_count([('physician_id', '=', record.id)])
            record.appointment_count = Appointment.search_count([('physician_id', '=', record.id)])
            record.prescription_count = Prescription.search_count([('physician_id', '=', record.id)])
            record.patient_count = Patient.search_count(
                ['|', ('primary_physician_id', '=', record.id), ('assignee_ids', 'in', record.partner_id.id)])

    consultaion_service_id = fields.Many2one('product.product', ondelete='restrict', string='Telehealth Service',
                                             default=1336 or False)
    followup_service_id = fields.Many2one('product.product', ondelete='restrict', string='Followup Service',
                                          default=1292 or False)
    appointment_duration = fields.Float('Consultation (min)', default=0.25)

    is_primary_surgeon = fields.Boolean(string='Primary Surgeon')
    signature = fields.Binary('Signature')
    hr_presence_state = fields.Selection(related='user_id.employee_id.hr_presence_state')
    appointment_ids = fields.One2many("hms.appointment", "physician_id", "Appointments")

    treatment_count = fields.Integer(compute='_phy_rec_count', string='# Treatments')
    appointment_count = fields.Integer(compute='_phy_rec_count', string='# Appointment')
    prescription_count = fields.Integer(compute='_phy_rec_count', string='# Prescriptions')
    patient_count = fields.Integer(compute='_phy_rec_count', string='# Patients')

    provider_number = fields.Char(string="Provider Number")
    prescriber_number = fields.Char(string="Prescriber Number")

    firstname = fields.Char("First name", index=True)
    lastname = fields.Char("Last name", index=True)
    name = fields.Char(
        compute="_compute_name",
        inverse="_inverse_name_after_cleaning_whitespace",
        required=False,
        store=True,
        readonly=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Add inverted names at creation if unavailable."""
        context = dict(self.env.context)
        for vals in vals_list:
            name = vals.get("name", context.get("default_name"))

            if name is not None:
                # Calculate the splitted fields
                inverted = self._get_inverse_name(
                    self._get_whitespace_cleaned_name(name)
                )
                for key, value in inverted.items():
                    if not vals.get(key) or context.get("copy"):
                        vals[key] = value

                # Remove the combined fields
                if "name" in vals:
                    del vals["name"]
                if "default_name" in context:
                    del context["default_name"]
        # pylint: disable=W8121
        return super(Physician, self.with_context(context)).create(vals_list)

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        result = super().default_get(fields_list)

        inverted = self._get_inverse_name(
            self._get_whitespace_cleaned_name(result.get("name", "")))

        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.model
    def _names_order_default(self):
        return "first_last"

    @api.model
    def _get_names_order(self):
        """Get names order configuration from system parameters.
        You can override this method to read configuration from language,
        country, company or other"""
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_names_order", self._names_order_default())
        )

    @api.model
    def _get_computed_name(self, lastname, firstname):
        """Compute the 'name' field according to splitted data.
        You can override this method to change the order of lastname and
        firstname the computed name"""
        order = self._get_names_order()
        if order == "last_first_comma":
            return ", ".join(p for p in (lastname, firstname) if p)
        elif order == "first_last":
            return " ".join(p for p in (firstname, lastname) if p)
        else:
            return " ".join(p for p in (lastname, firstname) if p)

    @api.depends("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for record in self:
            record.name = record._get_computed_name(record.lastname, record.firstname)

    def _inverse_name_after_cleaning_whitespace(self):
        """Clean whitespace in :attr:`~.name` and split it.

        The splitting logic is stored separately in :meth:`~._inverse_name`, so
        submodules can extend that method and get whitespace cleaning for free.
        """
        for record in self:
            # Remove unneeded whitespace
            clean = record._get_whitespace_cleaned_name(record.name)
            record.name = clean
            record._inverse_name()

    @api.model
    def _get_whitespace_cleaned_name(self, name, comma=False):
        """Remove redundant whitespace from :param:`name`.

        Removes leading, trailing and duplicated whitespace.
        """
        if isinstance(name, bytes):
            # With users coming from LDAP, name can be a byte encoded string.
            # This happens with FreeIPA for instance.
            name = name.decode("utf-8")

        try:
            name = " ".join(name.split()) if name else name
        except UnicodeDecodeError:
            # with users coming from LDAP, name can be a str encoded as utf-8
            # this happens with ActiveDirectory for instance, and in that case
            # we get a UnicodeDecodeError during the automatic ASCII -> Unicode
            # conversion that Python does for us.
            # In that case we need to manually decode the string to get a
            # proper unicode string.
            name = " ".join(name.decode("utf-8").split()) if name else name

        if comma:
            name = name.replace(" ,", ",")
            name = name.replace(", ", ",")
        return name

    @api.model
    def _get_inverse_name(self, name):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.

        This method can be easily overriden by other submodules.
        You can also override this method to change the order of name's
        attributes

        When this method is called, :attr:`~.name` already has unified and
        trimmed whitespace.
        """

        order = self._get_names_order()
        # Remove redundant spaces
        name = self._get_whitespace_cleaned_name(
            name, comma=(order == "last_first_comma")
        )
        parts = name.split("," if order == "last_first_comma" else " ", 1)
        if len(parts) > 1:
            if order == "first_last":
                parts = [" ".join(parts[1:]), parts[0]]
            else:
                parts = [parts[0], " ".join(parts[1:])]
        else:
            while len(parts) < 2:
                parts.append(False)
        return {"lastname": parts[0], "firstname": parts[1]}

    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        for record in self:
            parts = record._get_inverse_name(record.name)
            record.lastname = parts["lastname"]
            record.firstname = parts["firstname"]

    @api.constrains("firstname", "lastname")
    def _check_name(self):
        """Ensure at least one name is set."""
        for record in self:
            if not all(record.firstname or record.lastname):
                raise exceptions.EmptyNamesError(record)

    @api.model
    def _install_partner_firstname(self):
        """Save names correctly in the database.

        Before installing the module, field ``name`` contains all full names.
        When installing it, this method parses those names and saves them
        correctly into the database. This can be called later too if needed.
        """
        # Find records with empty firstname and lastname
        records = self.search([("firstname", "=", False), ("lastname", "=", False)])

        # Force calculations there
        # records._inverse_name()
        # _logger.info("%d partners updated installing module.", len(records))

    # Disabling SQL constraint givint a more explicit error using a Python
    # contstraint
    # _sql_constraints = [("check_name", "CHECK( 1=1 )", "Contacts require a name.")]

    def action_treatment(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms.acs_action_form_hospital_treatment")
        action['domain'] = [('physician_id', '=', self.id)]
        action['context'] = {'default_physician_id': self.id}
        return action

    def action_appointment(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms.action_appointment")
        action['domain'] = [('physician_id', '=', self.id)]
        action['context'] = {'default_physician_id': self.id}
        return action

    def action_prescription(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms.act_open_hms_prescription_order_view")
        action['domain'] = [('physician_id', '=', self.id)]
        action['context'] = {'default_physician_id': self.id}
        return action

    def action_patients(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms_base.action_patient")
        action['domain'] = ['|', ('primary_physician_id', '=', self.id), ('assignee_ids', 'in', self.partner_id.id)]
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
