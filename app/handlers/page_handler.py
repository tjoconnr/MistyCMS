#!/usr/bin/env python
from ._handler import BaseHandler

class PageHandler(BaseHandler):
    def get(self, route):
        if not route:
            route = "index"
        template_values = self.authorize(route=route, require_login=False)
        self.render("views/page/%s.html" % route, **template_values)



