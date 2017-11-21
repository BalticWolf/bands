import unittest
import Scraper


class TestPeriod(unittest.TestCase):
    """
    Tests if string representing periods are correctly transformed in dict
    """
    def test00_no_date(self):
        """Empty input returns a dictionary with empty string values"""
        self.assertEqual(Scraper.transform_period(''), {'Start': '', 'End': ''})

    def test01_single_date1(self):
        """A single 4-digits year gives Start and End"""
        self.assertEqual(Scraper.transform_period('1984'), {'Start': 1984, 'End': 1984})

    def test02_single_date2(self):
        """A single 4-digits year gives Start and End"""
        self.assertEqual(Scraper.transform_period('2001'), {'Start': 2001, 'End': 2001})

    def test03_present(self):
        """Test if string end year is correctly transformed in empty string"""
        self.assertEqual(Scraper.transform_period('2005-present'), {'Start': 2005, 'End': ''})

    def test04_partial_1900(self):
        """Test if year on 2 digits is correctly formed"""
        self.assertEqual(Scraper.transform_period('1992-95'), {'Start': 1992, 'End': 1995})

    def test05_partial_2000(self):
        """Test if year on 2 digits is correctly formed"""
        self.assertEqual(Scraper.transform_period('2011-16'), {'Start': 2011, 'End': 2016})

    # TO DO: test with 04 for 2004

    def test06_complete_dates(self):
        """4-digit years on both sides"""
        self.assertEqual(Scraper.transform_period('1999-2004'), {'Start': 1999, 'End': 2004})

    def test07_interrogation_1(self):
        """End year is correctly transformed in empty string"""
        self.assertEqual(Scraper.transform_period('2005-?'), {'Start': 2005, 'End': ''})

    def test08_interrogation_2(self):
        """Start year is correctly transformed in empty string"""
        self.assertEqual(Scraper.transform_period('?-2005'), {'Start': '', 'End': 2005})


class TestPeriods(unittest.TestCase):
    def test00_empty(self):
        """Empty list of periods returns an empty list"""
        self.assertEqual(Scraper.transform_periods([]), [])


if __name__ == '__main__':
    unittest.main()
