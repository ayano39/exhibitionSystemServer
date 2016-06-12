from django.test import TestCase
import unittest
from unittest import TestCase
from exhibitionSystem.views import *

class test_views(TestCase):
    def test_makeroute(self):
        interests=[1,1,1,1,1]
        id = 1
        a = make_route(1,interests)
        print(a.grade)
        print(a.path)

if __name__ == '__main__':
    unittest.main()
# Create your tests here.
