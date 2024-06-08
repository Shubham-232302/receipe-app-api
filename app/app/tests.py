from django.test import SimpleTestCase
from app.calc import add_nums

class CalcTests(SimpleTestCase):
    
    def test_add_nums(self):
        res = add_nums(9, 10)
        self.assertEqual(19, res)
