#!/usr/bin/env python
import webapp2

#-----------------------------------------------------------------------------
#
#   ** START APPLICATION **
#
#-----------------------------------------------------------------------------
from app.handlers import *
from app.constants import AUTH_LOGIN_URL
ROUTES = [
  ("/test/", TestHandler),
  (AUTH_LOGIN_URL, AuthHandler),
  ("/a/", AdminHandler),
  ("/a/(.*)/(.*)", AdminHandler),
  ("/!/(\d{16})/(.*)", WebsiteHandler),
  ("/api/(.*)", ApiHandler),
  ("/(.*)", PageHandler)
]

app = webapp2.WSGIApplication(ROUTES, debug=True)
