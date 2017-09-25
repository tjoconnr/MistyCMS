#!/usr/bin/env python
import logging
from datetime import datetime
from google.appengine.api import memcache

from ..models import Website, Asset
from ..constants import CACHE_SECONDS
from ._handler import BaseHandler

HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {% block header %}{% endblock %}
    </head>
  <body>
  {% block container %}{% endblock %}
  {% block footer %}{% endblock %}
  </body>
</html>
"""

class WebsiteHandler(BaseHandler):
    def get(self, website_id, path):
        before_render = datetime.now()

        website = Website.get_by_id(website_id)
        if not website:
            self.error(500)

        theme = self.request.get('theme', 'default')
        template = self.request.get('template', 'default')
        CACHE_KEY = "website:%s:%s:%s:%s" % (website_id, theme, template, path)

        # resp = None
        # if self.request.get('refresh') != None:
        # resp = memcache.get(CACHE_KEY)
        served = 'SERVER' if resp == None else 'CACHE'

        # template_values = {}
        # if not resp:
        template_values = self.authorize(path)
            # if theme:
            #     template_values['theme'] = Asset.get_by_id(theme).to_dict()

            # if template:
            #     template_values['template'] = Asset.get_by_id(template).to_dict()




        template_values['website'] = website.to_dict() if website else {}
        resp = self.render_string(html=HTML, **template_values)
        memcache.add(CACHE_KEY, resp, CACHE_SECONDS)

        self.response.write(resp)

        duration_ms = (datetime.now() - before_render).total_seconds()*1000

        self.response.write('\n<!-- Rendered from%s in %s milliseconds -->' % (served, duration_ms))


