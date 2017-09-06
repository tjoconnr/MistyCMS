#!/usr/bin/env python
import unittest

def flush():
    '''Fake method allowing Response to be passed into TestRunner'''
    pass

def render_tests(self):
    self.response.flush = flush
    self.response.headers['Content-Type'] = "text/plain"
    run_tests(stream=self.response)

def run_tests(stream=None):
    test_suites = []
    from specs import __all__ as TEST_SPECS

    for t in TEST_SPECS:
        s = unittest.TestLoader().loadTestsFromTestCase(t)
        test_suites.append(s)
    full_suite = unittest.TestSuite(test_suites)

    # Run test
    if stream:
        unittest.TextTestRunner(stream=stream, verbosity=2).run(full_suite)
    else:
        unittest.TextTestRunner(verbosity=2).run(full_suite)
