#!/usr/bin/env python
import webapp2
from ..tests.main import render_tests

class TestHandler(webapp2.RequestHandler):
    def get(self):
        render_tests(self)
