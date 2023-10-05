
from ast import literal_eval

import base64
import json
import logging
import math
import werkzeug

from odoo import http, tools, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.website_profile.controllers.main import WebsiteProfile
from odoo.exceptions import AccessError, ValidationError, UserError, MissingError
from odoo.http import request
from odoo.osv import expression
from odoo.tools import email_split


class SlidesFiler(WebsiteProfile):

    @http.route('/slides', type='http', auth="user", website=True, sitemap=True)
    def slides_channel_home(self, **post):
        """ Home page for eLearning platform. Is mainly a container page, does not allow search / filter. """
        channels_all = tools.lazy(lambda: request.env['slide.channel'].search(request.website.website_domain()))
        if not request.env.user._is_public():
            #If a course is completed, we don't want to see it in first position but in last
            channels_my = tools.lazy(lambda: channels_all.filtered(lambda channel: channel.is_member).sorted(lambda channel: 0 if channel.completed else channel.completion, reverse=True)[:3])
        else:
            channels_my = request.env['slide.channel']
        channels_popular = tools.lazy(lambda: channels_all.sorted('total_votes', reverse=True)[:3])
        channels_newest = tools.lazy(lambda: channels_all.sorted('create_date', reverse=True)[:3])

        achievements = tools.lazy(lambda: request.env['gamification.badge.user'].sudo().search([('badge_id.is_published', '=', True)], limit=5))
        if request.env.user._is_public():
            challenges = None
            challenges_done = None
        else:
            challenges = tools.lazy(lambda: request.env['gamification.challenge'].sudo().search([
                ('challenge_category', '=', 'slides'),
                ('reward_id.is_published', '=', True)
            ], order='id asc', limit=5))
            challenges_done = tools.lazy(lambda: request.env['gamification.badge.user'].sudo().search([
                ('challenge_id', 'in', challenges.ids),
                ('user_id', '=', request.env.user.id),
                ('badge_id.is_published', '=', True)
            ]).mapped('challenge_id'))

        users = tools.lazy(lambda: request.env['res.users'].sudo().search([
            ('karma', '>', 0),
            ('website_published', '=', True)], limit=5, order='karma desc'))

        render_values = self._slide_render_context_base()
        render_values.update(self._prepare_user_values(**post))
        render_values.update({
            'channels_my': channels_my,
            'channels_popular': channels_popular,
            'channels_newest': channels_newest,
            'achievements': achievements,
            'users': users,
            'top3_users': tools.lazy(self._get_top3_users),
            'challenges': challenges,
            'challenges_done': challenges_done,
            'search_tags': request.env['slide.channel.tag'],
            'slide_query_url': QueryURL('/slides/all', ['tag']),
            'slugify_tags': self._slugify_tags,
        })

        return request.render('website_slides.courses_home', render_values)