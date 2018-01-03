import unittest
from src.main import Scraper


class TestMember(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(
            Scraper.member_to_dict(""),
            None
        )

    def test_trailing_spaces(self):
        self.assertEqual(
            Scraper.member_to_dict('  Tomas Haake '),
            {'Name': 'Tomas Haake'}
        )

    def test_name_only(self):
        self.assertEqual(
            Scraper.member_to_dict("Stephen O'Malley"),
            {'Name': "Stephen O'Malley"}
        )

    def test_name_empty_aka(self):
        self.assertEqual(
            Scraper.member_to_dict('Joey Jordison []'),
            {'Name': 'Joey Jordison'}
        )

    def test_name_aka(self):
        self.assertEqual(
            Scraper.member_to_dict('Joey Jordison [#1]'),
            {'Name': 'Joey Jordison', 'Aka': '#1'}
        )

    def test_name_instruments(self):
        self.assertEqual(
            Scraper.member_to_dict('Tomas Haake (drums)'),
            {'Name': 'Tomas Haake', 'Instruments': 'drums'}
        )

    def test_name_aka_instruments(self):
        self.assertEqual(
            Scraper.member_to_dict('Joey Jordison [#1] (drums)'),
            {'Name': 'Joey Jordison', 'Instruments': 'drums', 'Aka': '#1'}
        )

    def test_name_empty_features(self):
        self.assertEqual(
            Scraper.member_to_dict('Joey Jordison ()'),
            {'Name': 'Joey Jordison'}
        )

    def test_name_features(self):
        self.assertEqual(
            Scraper.member_to_dict('Timo (drums, 2015-present)'),
            {'Name': 'Timo', 'Instruments': 'drums', 'Periods': [{'Start': 2015, 'End': ''}]}
        )


class TestPeriod(unittest.TestCase):
    """
    Tests if string representing periods are correctly transformed in dict
    """
    def test_empty(self):
        """Empty input returns a dictionary with empty string values"""
        self.assertEqual(
            Scraper.transform_period(''),
            None
        )

    def test_single_date1(self):
        """A single 4-digits year gives Start and End"""
        self.assertEqual(
            Scraper.transform_period('1984'),
            {'Start': 1984, 'End': 1984}
        )

    def test_single_date2(self):
        """A single 4-digits year gives Start and End"""
        self.assertEqual(
            Scraper.transform_period('2001'),
            {'Start': 2001, 'End': 2001}
        )

    def test_present(self):
        """Test if string end year is correctly transformed in empty string"""
        self.assertEqual(
            Scraper.transform_period('2005-present'),
            {'Start': 2005, 'End': ''}
        )

    def test_partial_1900(self):
        """Test if year on 2 digits is correctly formed"""
        self.assertEqual(
            Scraper.transform_period('1992-95'),
            {'Start': 1992, 'End': 1995}
        )

    def test_partial_2000(self):
        """Test if year on 2 digits is correctly formed"""
        self.assertEqual(
            Scraper.transform_period('2002-04'),
            {'Start': 2002, 'End': 2004}
        )

    def test_partial_2010(self):
        """Test if year on 2 digits is correctly formed"""
        self.assertEqual(
            Scraper.transform_period('2011-16'),
            {'Start': 2011, 'End': 2016}
        )

    def test_complete_dates(self):
        """4-digit years on both sides"""
        self.assertEqual(
            Scraper.transform_period('1999-2004'),
            {'Start': 1999, 'End': 2004}
        )

    def test_interrogation_1(self):
        """End year is correctly transformed in empty string"""
        self.assertEqual(
            Scraper.transform_period('2005-?'),
            {'Start': 2005, 'End': ''}
        )

    def test_interrogation_2(self):
        """Start year is correctly transformed in empty string"""
        self.assertEqual(
            Scraper.transform_period('?-2005'),
            {'Start': '', 'End': 2005}
        )


class TestPeriods(unittest.TestCase):
    def test_empty(self):
        """Empty list of periods returns an empty list"""
        self.assertEqual(
            Scraper.transform_periods(''),
            None
        )


if __name__ == '__main__':
    unittest.main()
