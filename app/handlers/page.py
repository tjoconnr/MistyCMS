#!/usr/bin/env python
from ._handler import BaseHandler

class PageHandler(BaseHandler):
    def get(self, endpoint):
        if not endpoint:
            self.redirect('/login', abort=True)
        template_values = self.authorize(endpoint=endpoint,
            require_login=False)
        self.render("views/page/%s.html" % endpoint, **template_values)
