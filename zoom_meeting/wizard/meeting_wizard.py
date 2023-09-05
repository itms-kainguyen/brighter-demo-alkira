# -*- coding: utf-8 -*-
##########################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>;)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
##########################################################################
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging
import requests
import json

_logger = logging.getLogger(__name__)

MEETING_TYPE_OPTION = [
    ('1', 'Instant meeting'),
    ('2', 'Scheduled meeting'),
    ('3', 'Recurring meeting with no fixed time'),
    ('8', 'Recurring meeting with a fixed time'),
]


class wizardMeeting(models.TransientModel):
    _name = "wizard.zoom"
    agenda = fields.Text("Agenda")
    alternative_hosts = fields.Text(string="Alternative Hosts")
    password = fields.Char("Password")
    host_video = fields.Boolean("Host Video")
    participant_video = fields.Boolean("Participant Video", default=True)
    joining_option = fields.Selection(
        [('joining_before_host', 'Join before Host'), ('waiting_room', "Waiting Room")], default='joining_before_host',
        string="Joining Option")
    mute_upon_entry = fields.Boolean("Mute Upon entry")
    watermark = fields.Boolean("Watermark")
    schedule_for_reminder = fields.Boolean(
        "Notify host and alternative host about the meeting cancellation via email", default=False)
    cancel_meeting_reminder = fields.Boolean(
        "Notify registrants about the meeting cancellation via email", default=False)
    meeting_type = fields.Selection(
        MEETING_TYPE_OPTION, string='Meeting Type', default='1', )

    def _calendar_active_id(self):
        return self.env['calendar.event'].browse(
            self._context.get('active_id'))

    def create_zoom_meeting(self):
        calendar_active_id = self._calendar_active_id()
        if calendar_active_id.partner_ids:
            meeting_invitees = []
            join_before_host = False
            waiting_room = False
            for email in calendar_active_id.partner_ids:
                meeting_invitees.append({"email": email.email})
            if self.joining_option == 'joining_before_host':
                join_before_host = 'true'
            else:
                waiting_room = 'true'
            meetingdetails = {"topic": calendar_active_id.name,
                              "type": int(self.meeting_type),
                              "start_time": str(calendar_active_id.start.date()) + 'T' + str(
                                  calendar_active_id.start.time()) + 'Z',
                              "duration": calendar_active_id.duration * 60,
                              "timezone": self.env.context.get('tz'),
                              "agenda": self.agenda,
                              "recurrence": {"type": 1,
                                             "repeat_interval": 1
                                             },
                              "settings": {"host_video": self.host_video,
                                           "email_notification": 'true',
                                           "participant_video": self.participant_video,
                                           "join_before_host": join_before_host,
                                           "waiting_room": waiting_room,
                                           "mute_upon_entry": self.mute_upon_entry,
                                           "watermark": self.watermark,
                                           #    "registrants_confirmation_email"
                                           "meeting_invitees": meeting_invitees,
                                           "audio": "voip",
                                           "auto_recording": "cloud"
                                           }
                              }
            if self.password:
                meetingdetails.update({
                    "password": self.password,
                })

            if self.alternative_hosts:
                meetingdetails.update({
                    "alternative_hosts": self.alternative_hosts,
                })
                calendar_active_id.alternative_hosts = self.alternative_hosts
            calendar_active_id.zoom_description = meetingdetails
            if (self.env.user).refresh_token:
                (self.env.user).refresh_access_token()
                access_token = (self.env.user).access_token


            elif (self.env.company).refresh_token:
                (self.env.company).refresh_access_token()
                access_token = (self.env.company).access_token
            else:
                raise UserError(_("First generate token in User or Company"))
            try:
                headers = {'authorization': 'Bearer ' + access_token,
                           'content-type': 'application/json'}
                r = requests.post('https://api.zoom.us/v2/users/me/meetings',
                                  headers=headers, data=json.dumps(meetingdetails))

                resp = json.loads(r.text)
                calendar_active_id.write({'meeting_id': resp.get('id', False), 'videocall_location': resp.get(
                    'join_url', False), 'start_meeting_url': resp.get('start_url', False),
                                          'password': resp.get('password', False)})
                template_id = self.env.ref('zoom_meeting.mail_template_meeting_invitation')
                template_id.send_mail(calendar_active_id.id, force_send=True)
                return self.env['wk.wizard.message'].genrated_message("Your zoom meeting has been created",
                                                                      name='Message')
            except:
                raise UserError(
                    _("There is a problem in fields data or access token, please check and try again "))
        else:
            raise UserError(_("Please add minimum one participant"))

    def update_zoom_meeting(self):
        join_before_host = False
        waiting_room = False
        calendar_active_id = self._calendar_active_id()
        if self.joining_option == 'joining_before_host':
            join_before_host = 'true'
        else:
            waiting_room = 'true'
        settings = {
            "audio": "voip",
            "auto_recording": "cloud"
        }

        if calendar_active_id.partner_ids:
            meetingdetails = {"topic": calendar_active_id.name,
                              "type": int(self.meeting_type),
                              "start_time": str(calendar_active_id.start.date()) + 'T' + str(
                                  calendar_active_id.start.time()) + 'Z',
                              "duration": calendar_active_id.duration * 60,
                              "timezone": self.env.context.get('tz'),
                              "recurrence": {"type": 1,
                                             "repeat_interval": 1
                                             },
                              "settings": settings
                              }
            if self.agenda:
                meetingdetails.update({"agenda": self.agenda})
            if self.password:
                meetingdetails.update({"password": self.password})
            if self.host_video:
                settings.update({"host_video": self.host_video})
            if self.participant_video:
                settings.update({"participant_video": self.participant_video})
            if join_before_host:
                settings.update({"join_before_host": join_before_host})
            else:
                settings.update({"waiting_room": waiting_room})
            if self.mute_upon_entry:
                settings.update({"mute_upon_entry": self.mute_upon_entry})
            if self.watermark:
                settings.update({"watermark": self.watermark})
            calendar_active_id.zoom_description = meetingdetails
            if (self.env.user).refresh_token:
                (self.env.user).refresh_access_token()
                access_token = (self.env.user).access_token
            elif (self.env.company).refresh_token:
                (self.env.company).refresh_access_token()
                access_token = (self.env.company).access_token
            else:
                raise UserError(_("First generate token in User or Company"))
            try:
                headers = {'authorization': 'Bearer ' + access_token,
                           'content-type': 'application/json'}
                response = requests.patch('https://api.zoom.us/v2/meetings/{}'.format(int(
                    calendar_active_id.meeting_id)), headers=headers, data=json.dumps(meetingdetails))
                if response.status_code == 204:
                    return self.env['wk.wizard.message'].genrated_message(
                        "Your zoom meeting ({}) has been updated".format(calendar_active_id.meeting_id), name='Message')
                elif response.status_code == 404:
                    return self.env['wk.wizard.message'].genrated_message(
                        "User is not found else meeting has been deleted", name='Message')
                else:
                    calendar_active_id.meeting_id = False
                    return self.env['wk.wizard.message'].genrated_message(
                        "There is a problem please confirm that meeting url is active or meeting is not expired",
                        name='Message')
            except:
                return self.env['wk.wizard.message'].genrated_message(
                    "There is a problem in fields data or access token, please check and try again", name='Message')

    def delete_zoom_meeting(self):
        calendar_active_id = self._calendar_active_id()
        if (self.env.user).refresh_token:
            (self.env.user).refresh_access_token()
            access_token = (self.env.user).access_token
        elif (self.env.company).refresh_token:
            (self.env.company).refresh_access_token()
            access_token = (self.env.company).access_token
        else:
            raise UserError(_("First generate token in User or Company"))
        try:
            headers = {'authorization': 'Bearer ' + access_token,
                       'content-type': 'application/json'}
            params = {'schedule_for_reminder': self.schedule_for_reminder,
                      'cancel_meeting_reminder': self.cancel_meeting_reminder}
            response = requests.delete('https://api.zoom.us/v2/meetings/{}'.format(
                calendar_active_id.meeting_id), headers=headers, params=params)
            if response.status_code == 204:
                calendar_active_id.meeting_id = False
                if self.schedule_for_reminder and calendar_active_id.alternative_hosts:
                    template_id = self.env.ref('zoom_meeting.mail_template_meeting_delete_alternative_hosts')
                    template_id.send_mail(calendar_active_id.id, force_send=True)
                elif self.cancel_meeting_reminder:

                    template_id = self.env.ref('zoom_meeting.mail_template_meeting_delete_attendees')
                    _logger.info("====================1==================%s" % template_id.email_to)
                    _logger.info("====================1==================%s" % template_id.email_from)
                    template_id.send_mail(calendar_active_id.id, force_send=True)
                return self.env['wk.wizard.message'].genrated_message("Your zoom meeting has been deleted",
                                                                      name='Message')
            elif response.status_code == 404:
                return self.env['wk.wizard.message'].genrated_message(
                    "User is not found else meeting has been deleted already", name='Message')
            else:
                calendar_active_id.meeting_id = False
                return self.env['wk.wizard.message'].genrated_message(
                    "There is a problem please confirm that all details are proper and user belong to account",
                    name='Message')

        except:
            return self.env['wk.wizard.message'].genrated_message(
                "There is a problem in fields data or access token, please check and try again", name='Message')
