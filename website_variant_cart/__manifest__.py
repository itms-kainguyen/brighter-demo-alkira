# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
{
  "name"                 :  "Website Multi Variant Add to Cart",
  "summary"              :  """This module allows customer to add multiple product variants with different quantities in cart at once.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Multi-Variant-Add-to-Cart.html",
  "description"          :  """https://webkul.com/blog/odoo-website-multi-variant-add-to-cart/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_variant_cart",
  "depends"              :  ['website_sale'],
  "data"                 :  [
                             'views/multi_variant_template.xml',
                             'views/product_template_view.xml',
                            ],
  "demo"                 :  [],
  "images"               :  ['static/description/Banner.gif'],
  "application"          :  True,
  "assets"               : {
                            'web.assets_frontend': ['website_variant_cart/static/src/**/*',]
                            },
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}