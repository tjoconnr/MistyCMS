#!/usr/bin/env python
import logging

from ..models import Website, User, Account
from ._handler import BaseHandler
from ..setup import create_default_assets

class ApiHandler(BaseHandler):
    def post(self, endpoint):
        logging.info(self.request.POST)
        template_values = self.authorize(endpoint=endpoint)
        if not template_values['account']:
            self.error(500)
            return

        if endpoint == "install":
            create_default_assets()

        if endpoint == "account":

            if self.request.get('account-name'):
                Account.update(account_id=template_values['account']['id'],
                    name=self.request.get('account-name'),
                    account_type=self.request.get('account-type'))
            if self.request.get('user-name'):
                User.update(user_id=template_values['user']['id'],
                    name=self.request.get('user-name'))

        if endpoint == "website":
            website_key = Website.update(account_id=template_values['account']['id'],
                website_id=self.request.get('website-id',None),
                name=self.request.get('website-name'),
                description=self.request.get('website-description'),
                title=self.request.get('website-title'),
                subdomain=self.request.get('website-subdomain'))
            if self.request.get('create'):
                self.redirect('/a/sites/dashboard?id=%s' % website_key.id(), abort=True)


        if self.request.get('redirect'):
            self.redirect(self.request.get('redirect'))
        else:
            self.redirect(self.request.environ.get('HTTP_REFERER'))


