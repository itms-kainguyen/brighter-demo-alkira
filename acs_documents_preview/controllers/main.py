# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.tools.translate import _


class AcsImageZoom(http.Controller):

    @http.route(['/my/acs/image/<string:model>/<int:record>'], type='http', auth="user", website=True, sitemap=False)
    def acs_image_preview(self, model=False, record=False, **kwargs):
        record = request.env[model].browse([record])
        attachments = request.env['ir.attachment'].search([
            ('res_model', '=', record._name),
            ('res_id', '=', record.id),
            ('mimetype', 'in', ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'])
        ])

        attachments_patient_document = request.env['patient.document'].search([
            ('res_model', '=', record._name),
            ('res_id', '=', record.id),
            ('mimetype', 'in', ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'])
        ])

        for attachment in attachments_patient_document:
            ir_att = request.env['ir.attachment'].browse(attachment.ir_attachment_id.id)
            attachments += ir_att

        attachments_treatment = None
        if record._name == 'hms.treatment':
            attachments_treatment = request.env['ir.attachment'].search([
                '&', '|',
                ('id', 'in', record.attachment_before_ids.ids),
                ('id', 'in', record.attachment_after_ids.ids),
                ('mimetype', 'in', ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'])
            ])
            for attachment_treat in attachments_treatment:
                ir_att = request.env['ir.attachment'].browse(attachment_treat.id)
                attachments += ir_att

        return request.render("acs_documents_preview.acs_image_preview", {'attachments': attachments})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: