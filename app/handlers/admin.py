#!/usr/bin/env python
import logging
from datetime import datetime

from ..models import Website
from .. import setup
from ._handler import BaseHandler

class AdminHandler(BaseHandler):

    def get(self, endpoint=None, route=None):
        logging.info('Endpoint: %s, Route: %s' % (endpoint, route))
        before_render = datetime.now()

        if not endpoint:
            endpoint = "home"
        if not route:
            route = "index"

        template_values = self.authorize(endpoint=endpoint, route=route)

        # if not endpoint and template_values['websites']:
        #     self.redirect('/a/sites/dashboard?id=%s' % template_values['websites'][0]['id'], abort=True)



        # if not template_values['websites'] and endpoint not in ["setup", "sites"]:
        #     self.redirect('/a/sites/create', abort=True)

        website = None
        item_id = self.request.get('id')
        if endpoint == "sites" and item_id:
            website = Website.get_website(item_id)
            if not website:
                self.redirect('/500')

        logging.info("AdminHandler:%s:%s:%s" % (endpoint, item_id, route))

        template_values['website'] = website.to_dict() if website else {}
        self.render("views/admin/%s/%s.html" % (endpoint, route), **template_values)
        #self.response.write('\n<!-- Rendered in %s seconds -->' % (datetime.now() - before_render).total_seconds())

