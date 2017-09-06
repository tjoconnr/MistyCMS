#!/usr/bin/env python
from ._handler import BaseHandler
from app.models import Account, User, Menu
from app import setup

class AppHandler(BaseHandler):

    def get(self, route):
        if not route:
            self.redirect('/a/home', abort=True)
        template_values = self.authorize(route=route)
        self.render("views/app/%s.html" % route, **template_values)

    def post(self, route):

        if route == "admin":
            setup.create_default_assets()
            self.redirect('/a/admin', abort=True)

        if route == "setup":
            template_values = self.authorize(route=route)
            user_id = template_values['user']['id']
            account_id = template_values['account']['id']
            if not user_id:
                self.error(500)
                return

            User.update(user_id=user_id,
                name=self.request.get("name"))

            Account.update(account_id=account_id,
                name=self.request.get("company"),
                website=self.request.get("website"))

            menu = Menu.list(account_id=account_id)[0]

        self.redirect('/a/menu?menu_id=%s' % menu.key.id())
