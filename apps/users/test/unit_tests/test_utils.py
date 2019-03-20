# -*- coding:utf-8 -*-
# __author__ = 'zhan'
# __date__ = '18-4-14 下午10:02'

from django.test import TestCase
from django.test.client import RequestFactory

from users.utils.utlis import get_client_ip_from_request


class GetIPAddressTest(TestCase):
    """
    get_ip_address_from_request函数的测试
    """
    def setUp(self):
        super(GetIPAddressTest, self).setUp()
        self.rf = RequestFactory()

    def test_get_client_ip_from_request(self):
        test_ip = '10.10.61.3'
        request = self.rf.get('/', REMOTE_ADDR=test_ip)
        client_ip = get_client_ip_from_request(request)
        print 'test_get_client_ip_from_request'
        self.assertEqual(client_ip, test_ip)

    def test_get_client_ip_from_request_without_ip(self):
        request = self.rf.get('/')
        client_ip = get_client_ip_from_request(request)
        print "test_get_client_ip_from_request_without_ip"
        self.assertEquals(client_ip, None)

    def tearDown(self):
        print 'test over'