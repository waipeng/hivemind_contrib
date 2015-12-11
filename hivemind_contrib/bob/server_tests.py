#!/usr/bin/env python

import unittest, os, re
import requests

# This is either very clever or very stupid
class ServerTestCase(unittest.TestCase):
    def __init__(self, testname, server):
        self.server = server
        super(ServerTestCase, self).__init__(testname)

    # test if server is active
    def test_server_status_active(self):
        self.assertEqual(self.server.status, "ACTIVE", 
                msg="Server status is not ACTIVE")

    # test for active port state
    def test_port_state_active(self):
        interfaces = self.server.interface_list()
        self.assertEqual(interfaces[0].port_state, "ACTIVE", 
                msg="Port state is not ACTIVE")

    # test for instance missing images
    # useful for cases when instances are still running but the image is gone
    # from /var/lib/nova/instances
    # Note(jake): might not be valid anymore, removing from list of tests
    def test_image_not_found(self):
        if not hasattr(self.server, 'fault'):
            return True
        msg = self.server.fault['message']
        m = re.match(r"^Image (.)+ could not be found.$", msg)
        self.assertIsNone(m, msg="Image not found")

    # test if console logs returns anything
    def test_server_console_log(self):
        self.assertNotEqual(len(self.server.get_console_output()), 0,
                msg="Console log has no output")

    # test get vnc console
    def test_server_get_novnc_url(self):
        console = self.server.get_vnc_console('novnc')
        self.assertTrue(console, msg="Unable to get novnc URL")

    # test novnc
    # TODO(jake): figure out how to test if console is working
    def test_server_novnc(self):
        console = self.server.get_vnc_console('novnc')
        r = requests.get(console['console']['url'])
        self.assertEqual(r.status_code, 200,
                msg="novnc url response status code not 200")


def run(server):
    suite = unittest.TestSuite()
    suite.addTest(ServerTestCase('test_server_status_active', server))
    suite.addTest(ServerTestCase('test_port_state_active', server))
    suite.addTest(ServerTestCase('test_server_console_log', server))
    suite.addTest(ServerTestCase('test_server_get_novnc_url', server))
    suite.addTest(ServerTestCase('test_server_novnc', server))

    # make unittest run quietly
    stream = open(os.devnull, 'w')

    testresult = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
    return testresult
