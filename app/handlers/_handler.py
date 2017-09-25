#!/usr/bin/env python
import webapp2
import json
from datetime import datetime

from jinja2 import TemplateNotFound
from google.appengine.api import users
from webapp2_extras import jinja2

from ..constants import AUTH_LOGIN_URL, AUTH_LOGOUT_URL, AUTH_KNOWN_EMAILS, ENV
from ..models import Account, Asset, Post, User, Website
from ..utils import gravatar

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        '''
        Returns a Jinja2 renderer cached in the app registry.
        The filters.update allows you to add custom functions to your templates
        e.g. {{ user_email|gravatar(100) }}
        '''
        jinja_obj = jinja2.get_jinja2(app=self.app)
        jinja_obj.environment.filters.update({
             "gravatar": gravatar
        })
        return jinja_obj

    def authorize(self, endpoint="", route="", require_login=True, **template_values):
        '''
        Authorize with the Google AppEngine Framework, which uses GMail or
        GSuite for Business.
        '''

        user = None
        user_email = None
        if users.get_current_user():
            user_email = users.get_current_user().email()
            user = User.get_user(user_email)

        if require_login and not user:
            self.redirect(users.create_login_url(self.request.url))

        account = None
        account_id = None
        sites = []
        if user:
            account_id = user.account.id()
            account = user.account.get()
            sites = Website.list(account_id=account_id)

        template_values = {}
        template_values['user'] = user.to_dict() if user else {}
        template_values['account'] = account.to_dict() if account else {}
        template_values['websites'] = [w.to_dict() for w in sites] if sites else []
        template_values['env'] = ENV
        template_values['app'] = {
            'user_email': user_email,
            'endpoint': endpoint,
            'route': route,
            'is_admin': users.is_current_user_admin(),
            'logout_url': users.create_logout_url(AUTH_LOGOUT_URL),
            'login_url': users.create_login_url(AUTH_LOGIN_URL)
        }

        if users.is_current_user_admin():
            template_values['all'] = json.dumps(template_values, indent=2, sort_keys=True)

        return template_values

    def render(self, _template, **template_values):
        # Renders a Jinja2 template and writes the result to the response.
        try:
            rv = self.jinja2.render_template(_template, **template_values)
            self.response.write(rv)
        except TemplateNotFound:
            self.redirect("/404?path=%s" % self.request.url)

    def render_string(self, html, **template_values):
        return self.jinja2.environment.from_string(html).render(**template_values)
        self.response.write(rv)
