#!/usr/bin/env python
import webapp2
import json
from datetime import datetime

from jinja2 import TemplateNotFound
from google.appengine.api import users
from webapp2_extras import jinja2

from app.constants import LOGIN_URL, LOGOUT_URL, SETUP_URL, ASSET_TYPES
from app.models import Account, Asset, Menu, MenuItem, User
from app.setup import create_user

from app import utils


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        '''
        Returns a Jinja2 renderer cached in the app registry.

        The filters.update allows you to add custom functions to your templates e.g. {{ user_email|gravatar(100) }}

        '''
        jinja_obj = jinja2.get_jinja2(app=self.app)
        jinja_obj.environment.filters.update({
             "gravatar": utils.gravatar
        })
        return jinja_obj

    def get_user(self, template_values={}):
        user_email = None
        account = {}
        account_id = None
        user = {}
        menus = []
        assets = []

        if users.get_current_user():
            user_email = users.get_current_user().email()
            user = User.get_user(email=user_email)

        if user:
            account_id = user.account.id()
            account = Account.get_account(account_id=account_id)
            menus = Menu.list(account_id=account_id)
            assets = Asset.get_assets(account_id=account_id)

        template_values['app'] = {
            'user_email': user_email
        }
        template_values['user'] = user.to_dict() if user else {}
        template_values['account'] = account.to_dict() if account else {}
        template_values['menus'] = [m.to_dict() for m in menus] if menus else []
        template_values['assets'] = [a.to_dict() for a in assets] if assets else []
        return user

    def authorize(self, route, require_login=True, **template_values):
        '''Authorize with the Google AppEngine Framework, which uses GMail or GSuite for Business.'''
        template_values = {}
        user = self.get_user(template_values=template_values)

        # Not Logged In
        if not users.get_current_user() and require_login:
            self.redirect(users.create_login_url(self.request.url))

        # Logged In, New Account
        if users.get_current_user() and not user and require_login:
            create_user(email=users.get_current_user().email())
            self.redirect(SETUP_URL, abort=True)


        if self.request.get("asset_id"):
            template_values['asset'] = Asset.get_by_id(self.request.get("asset_id")).to_dict()

        if self.request.get("menu_id"):
            menu_id = long(self.request.get("menu_id"))
            menu = Menu.get_menu(menu_id=menu_id)

            if menu.theme:
                template_values['theme'] = menu.theme.get().to_dict()

            if menu.template:
                template_values['template'] = menu.template.get().to_dict()

            template_values['menu'] = menu.to_dict()
            template_values['menu_items'] = [m.to_dict() for m in MenuItem.list(menu_id=menu_id)]

        template_values['app']['route'] = route
        template_values['app']['is_admin'] = users.is_current_user_admin()
        template_values['app']['logout_url'] = users.create_logout_url(LOGOUT_URL)
        template_values['app']['login_url'] = users.create_login_url(LOGIN_URL)


        if route == "admin":
            template_values['all'] = json.dumps(template_values, indent=2, sort_keys=True)

        return template_values

    def render(self, _template, **template_values):
        # Renders a Jinja2 template and writes the result to the response.
        try:
            rv = self.jinja2.render_template(_template, **template_values)
            self.response.write(rv)
        except TemplateNotFound:
            self.error(404)

    def render_string(self, html, **template_values):
        return self.jinja2.environment.from_string(html).render(**template_values)
        self.response.write(rv)
