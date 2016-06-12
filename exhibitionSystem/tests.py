import unittest
from unittest import TestCase
from exhibitionSystem.views import *

class TestGet_max_gra(TestCase):

    """
    def test_get_max_gra(self):
        path = []
        R1 = RouteInfo(11,path)
        R2 = RouteInfo(10, path)
        R3 = RouteInfo(15, path)
        R4 = RouteInfo(2, path)
        R5 = RouteInfo(3, path)
        all_3_route = [R1,R2,R3,R4,R5]
        a = get_max_gra(all_3_route)
        print(all_3_route.index(a))
        self.assertEqual(a,R3,"get_max_grade unsuccess")


    def test_grade_cal_3(self):
        path=[1,2]
        route = RouteInfo(15,path)
        inter=[1,1,2,1,1]
        grades=[0,0,5,0,0]
        r = grade_cal_3(route,inter,grades)
        self.assertEqual(r,5,"grade_cal_3 is not correct")

    def test_booth_grade(self):
        id =1
        a = get_booth_grades(id)
        b = [0,1,2,1,1]
        self.assertEqual(a,b,"No")
    """

    def test_makeroute(self):
        interest = [1,1,1,1,1]
        booth_id = 1
        a = make_route(booth_id,interest)
        print(a.grade)
        print(a.path)
    """
    def test_connid(self):
        con_boo_id = booth_conn.objects.filter(B1=1)
        a = get_conn_id(con_boo_id)
        print(a)
    """
if __name__ == '__main__':
    unittest.main()

# Create your tests here.
