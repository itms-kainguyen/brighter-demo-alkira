# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
import pytz
import uuid
from babel.dates import format_datetime
from datetime import  datetime
from odoo.addons.payment.controllers.portal import PaymentPortal
from odoo.osv.expression import  OR
from odoo import http, _
from odoo.http import request
from odoo.tools import  DEFAULT_SERVER_DATETIME_FORMAT as dtf
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools.misc import get_lang
from odoo.exceptions import ValidationError


class WebsiteSale(WebsiteSale):
    def _get_search_order(self, post):
        # OrderBy will be parsed in orm and so no direct sql injection
        # id is added to be sure that order is a unique sort key
        order = post.get('order') or request.env['website'].get_current_website().shop_default_sort
        return ' priority desc, is_published desc, %s, id desc' % order

