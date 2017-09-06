#!/usr/bin/env python
import webapp2

#-----------------------------------------------------------------------------
#
#   ** START APPLICATION **
#
#-----------------------------------------------------------------------------
from app.handlers import *

ROUTES = [
  ("/a/test", TestHandler),
  ("/a/(.*)", AppHandler),
  ("/api/(.*)", ApiHandler),
  ("/(.*)", PageHandler),
]

app = webapp2.WSGIApplication(ROUTES, debug=True)
