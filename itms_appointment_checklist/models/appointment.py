# coding: utf-8

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

STAGEVALIDATIONERRORMESSAGE = _(u"""Please enter check list for the Medical Treatment Checklist '{0}'!
You can't change this Appointment state until you confirm all jobs have been done.""")


class Appointment(models.Model):
    _inherit = 'hms.appointment'

    def _default_appointment_group_id(self):
        return self.env['appointment.group'].search([('member_ids', 'in', [self.env.user.id])], limit=1)

    @api.depends("appointment_group_id", "appointment_group_id.check_line_ids",
                 "appointment_group_id.check_line_ids.state", "check_list_line_ids", "state")
    def _compute_check_list_len(self):
        """
        Compute method for 'check_list_len', 'todo_check_ids', and 'checklist_progress'
        """
        for order in self:
            total_check_points = order.appointment_group_id.check_line_ids.filtered(
                lambda line: line.state == order.state)
            check_list_len = len(total_check_points)
            order.check_list_len = check_list_len
            order.checklist_progress = check_list_len and (len(order.check_list_line_ids) / check_list_len) * 100 or 0.0
            todo_check_ids = total_check_points - order.check_list_line_ids
            order.todo_check_ids = [(6, 0, todo_check_ids.ids)]

    READONLY_CONFIRMED_STATES = {'confirm': [('readonly', True)], 'in_consultation': [('readonly', True)],
                                 'pause': [('readonly', True)], 'to_invoice': [('readonly', True)],
                                 'waiting': [('readonly', True)], 'cancel': [('readonly', True)],
                                 'done': [('readonly', True)]}

    check_list_line_ids = fields.Many2many(
        "appointment.check.item",
        "appointment_check_item_rel_table",
        "appointment_id",
        "corder_check_item_id",
        string="Check list",
        help="Confirm that you finished all the points. Otherwise, you would not be able to move the order forward",
    )
    check_list_history_ids = fields.One2many(
        "appointment.checklist.history",
        "appointment_id",
        string="History",
    )
    check_list_len = fields.Integer(
        string="Total points",
        compute=_compute_check_list_len,
        store=True,
    )
    todo_check_ids = fields.Many2many(
        "appointment.check.item",
        "appointment_check_item_rel_table_todo",
        "appointment_id_todo",
        "corder_check_item_id_todo",
        string="Check List To-Do",
        compute=_compute_check_list_len,
        store=True,
    )
    checklist_progress = fields.Float(
        string="Progress",
        compute=_compute_check_list_len,
        store=True,
    )
    appointment_group_id = fields.Many2one("appointment.group", default=_default_appointment_group_id,
                                           states=READONLY_CONFIRMED_STATES,
                                           string="Appointment Group")

    @api.model
    def create(self, vals):
        order_id = super(Appointment, self).create(vals)
        if vals.get("check_list_line_ids"):
            changed_items = self.env["appointment.check.item"].browse(vals.get("check_list_line_ids")[0][2])
            changed_items._check_cheklist_rights()
            order_id._register_history(changed_items)
        return order_id

    def write(self, vals):
        if vals.get("check_list_line_ids") and not self.env.context.get("automatic_checks"):
            new_check_line_ids = self.env["appointment.check.item"].browse(vals.get("check_list_line_ids")[0][2])
            for order in self:
                old_check_line_ids = order.check_list_line_ids
                to_add_items = (new_check_line_ids - old_check_line_ids)
                to_remove_items = (old_check_line_ids - new_check_line_ids)
                changed_items = to_add_items | to_remove_items
                changed_items._check_cheklist_rights()
                order._register_history(to_add_items, "done")
                order._register_history(to_remove_items, "reset")
        # 2
        if vals.get("state"):
            self._check_checklist_complete(vals)
            self.sudo()._recover_filled_checklist(vals.get("state"))

        return super(Appointment, self).write(vals)

    def _register_history(self, changed_items, done_action="done"):
        for order in self:
            for item in changed_items:
                history_item_vals = {
                    "appointment_id": order.id,
                    "check_list_id": item.id,
                    "done_action": done_action,
                }
                self.env["appointment.checklist.history"].create(history_item_vals)

    def _check_checklist_complete(self, vals):
        for order in self:
            team_id = self.env["appointment.group"].browse(vals.get("group_id") or order.appointment_group_id.id)
            no_needed_states = team_id.no_stages_ids.mapped("state")
            if vals.get("state") not in no_needed_states:
                entered_len = vals.get("check_list_line_ids") and len(vals.get("check_list_line_ids")) or \
                              len(order.check_list_line_ids)
                required_len = vals.get("check_list_len") and vals.get("check_list_len") or order.check_list_len
                if entered_len != required_len:
                    raise ValidationError(STAGEVALIDATIONERRORMESSAGE.format(order.name))

    def _recover_filled_checklist(self, state):
        for order in self:
            to_recover = []
            already_considered = []
            for history_item in order.check_list_history_ids:
                check_item_id = history_item.check_list_id
                if check_item_id.state == state \
                        and check_item_id.should_be_reset \
                        and check_item_id.id not in already_considered \
                        and history_item.done_action == "done":
                    to_recover.append(check_item_id.id)
                already_considered.append(check_item_id.id)
            order.with_context(automatic_checks=True).check_list_line_ids = [(6, 0, to_recover)]
