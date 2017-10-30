import unittest
import Main


class TestPeriod(unittest.TestCase):
    """
    Tests if string representing periods are correctly transformed in dict
    """
    def test00_no_date(self):
        self.assertEqual(Main.transform_period(''), {})

    def test01_single_date1(self):
        self.assertEqual(Main.transform_period('1984'), {'Start': 1984, 'End': 1984})

    def test02_single_date2(self):
        self.assertEqual(Main.transform_period('2001'), {'Start': 2001, 'End': 2001})

    def test03_present(self):
        self.assertEqual(Main.transform_period('2005-present'), {'Start': 2005})

    def test04_partial_1900(self):
        self.assertEqual(Main.transform_period('1992-95'), {'Start': 1992, 'End': 1995})

    def test05_partial_2000(self):
        self.assertEqual(Main.transform_period('2011-16'), {'Start': 2011, 'End': 2016})

    def test06_complete_dates(self):
        self.assertEqual(Main.transform_period('1999-2004'), {'Start': 1999, 'End': 2004})


if __name__ == '__main__':
    unittest.main()
