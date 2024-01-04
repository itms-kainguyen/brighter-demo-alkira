# -*- coding: utf-8 -*-

from odoo import http, fields, _
from odoo.http import request
from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID

class ACSHms(http.Controller):

    @http.route(['/validate/prescriptionorder/<prescription_unique_code>'], type='http', auth="public", website=True, sitemap=False)
    def prescription_details(self, prescription_unique_code, **post):
        if prescription_unique_code:
            prescription = request.env['prescription.order'].sudo().search([('unique_code','=',prescription_unique_code)], limit=1)
            if prescription:
                return request.render("acs_hms.acs_prescription_details", {'prescription': prescription})
        return request.render("acs_hms.acs_no_details")

    @http.route('/appointment/confirm', type='http', auth="user")
    def accept_appointment(self, token, id, **kwargs):
        token = token or request.httprequest.args.get('access_token')
        app = request.env['hms.appointment'].sudo().search([
            ('access_token', '=', token),
            ('state', '!=', 'checkin')])
        app.appointment_confirm()
        return request.redirect('/my/appointments')

    @http.route('/appointment/decline', type='http', auth="user")
    def decline_appointment(self, token, id, **kwargs):
        token = token or request.httprequest.args.get('access_token')
        app = request.env['hms.appointment'].sudo().search([
            ('access_token', '=', token),
            ('state', '!=', 'checkin')])
        app.appointment_cancel()
        return request.redirect('/my/appointments')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: