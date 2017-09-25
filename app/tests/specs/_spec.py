#!/usr/bin/env python
import webapp2
import unittest

class BaseTestCase(unittest.TestCase):
    '''
    This base class performs setup for Request Handler testing, and should
    by implemented by a child TestCase class for each API module.
    '''
    def setUp(self):
    	from main import ROUTES
        self.app = webapp2.WSGIApplication(ROUTES)
        if not self.app:
        	self.fail()
