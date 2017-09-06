#!/usr/bin/env python
from ._test import BaseTestCase

class PageHandlerTests(BaseTestCase):
    def testHomepage(self):
    	resp = self.app.get_response('/')
    	self.assertEqual(resp.status_int, 200)

    def testNotFound(self):
    	resp = self.app.get_response('/this-should-not-work')
    	self.assertEqual(resp.status_int, 404)
