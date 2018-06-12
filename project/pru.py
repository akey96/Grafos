
import unittest
from project.controller.exception import CapacityNotAllowed

class Yo():
    def __init__(self, a):
        self.a = a

class MyTestCase(unittest.TestCase):

    def test_01(self):
        a = Yo(1)
        b = a
        c = Yo(1)
        self.assertIs(a,b)
        self.assertIsNot(a,c)

    def test_02(self):

        a = [1,2,3]
        self.assertIn(1,a)

    def test_03(self):
        self.assertIsInstance(1,int)


if __name__ == '__main__':
    unittest.main()