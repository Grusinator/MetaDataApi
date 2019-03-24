import unittest
from urllib import parse


class TestUrlLib(unittest.TestCase):

    def test_urljoin(self):
        expected = "test.com/api/objects"

        base_url = "test.com/api/"

        endpoint = "objects"

        res = parse.urljoin(base_url, endpoint)
        self.assertEqual(expected, res)

    def test_urljoin2(self):
        expected = "test.com/api/objects/"

        base_url = "test.com/api/"

        endpoint = "objects/"

        res = parse.urljoin(base_url, endpoint)
        self.assertEqual(expected, res)
