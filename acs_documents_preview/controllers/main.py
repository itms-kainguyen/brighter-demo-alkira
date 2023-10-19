# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.tools.translate import _


class AcsImageZoom(http.Controller):

    @http.route(['/my/acs/image/<string:model>/<int:record>'], type='http', auth="user", website=True, sitemap=False)
    def acs_image_preview(self, model=False, record=False, **kwargs):
        record = request.env[model].browse([record])
        attachments = request.env['patient.document'].search([
            ('res_model', '=', record._name),
            ('res_id', '=', record.id),
            ('mimetype', 'in', ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'])
        ])

        return request.render("acs_documents_preview.acs_image_preview", {'attachments': attachments})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: