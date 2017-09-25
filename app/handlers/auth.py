#!/usr/bin/env python
from ._handler import BaseHandler
from ..auth import create_user

class AuthHandler(BaseHandler):
    def get(self):
        template_values = self.authorize(endpoint="authorize")
        if not template_values['user']:
            create_user()
            self.redirect('/a/setup/', abort=True)
        self.redirect('/a/')

