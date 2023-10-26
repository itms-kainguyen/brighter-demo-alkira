# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart/update/multi/variant'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_multi_variant(self,data,**post):
        for i in range(len(data)):
            self.cart_update(
                product_id = data[i]['product_id'],
                add_qty = data[i]['add_qty'],
                product_custom_attribute_values = data[i]['product_custom_attribute_values'],
            )
        return {'redirect_url' : '/shop/cart'}

    @http.route(['/vc/shop/get_unit_price'], type='json', auth="public", methods=['POST'], website=True)
    def vc_get_unit_price(self, product_ids, add_qty, **kw):
        cntx = {'quantity': add_qty, 'website_id': request.website.id}
        products = request.env['product.product'].with_context(cntx).browse(product_ids)
        return {product.id: product._get_combination_info_variant().get('price') for product in products}
