#!/usr/bin/env python
import logging
from datetime import datetime
from google.appengine.api import memcache

from ._handler import BaseHandler
from app.models import Asset
from app.constants import CACHE_SECONDS

class CastHandler(BaseHandler):
    def get(self):
        before_render = datetime.now()

        menu_id = self.request.get('menu_id')
        theme = self.request.get('theme')
        template = self.request.get('template')
        CACHE_KEY = "menu:%s:%s:%s" % (menu_id, theme, template)

        resp = None
        if not self.request.get('refresh'):
            resp = memcache.get(CACHE_KEY)

        served = 'from server' if resp == None else 'from cache (%s)' % CACHE_KEY

        if not resp:
            template_values = self.authorize(route="cast")
            if theme:
                template_values['theme'] = Asset.get_by_id(theme).to_dict()

            if template:
                template_values['template'] = Asset.get_by_id(template).to_dict()

            resp = self.render_string(html=template_values['template']['content'], **template_values)
            memcache.add(CACHE_KEY, resp, CACHE_SECONDS)

        after_render = datetime.now()
        duration = (after_render - before_render).total_seconds()

        self.response.write(resp)
        self.response.write('\n<!-- Rendered %s in %s seconds -->' % (served, duration))

