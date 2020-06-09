"""
Unit test for named function
"""
import unittest
from data515_project.kc_real_estate import aggregate_by_date

aggregated_by_date = aggregate_by_date()
aggregated_by_date_cols = aggregated_by_date.columns

# Define a class in which the tests will run
class TestAggByZip(unittest.TestCase):
    """
    This implements the four test methods below.

    """

    # Each method in the class to execute a test

    def test_date_type(self):
        """
        test that function output dataframe index is of
        datetime type
        """
        self.assertTrue(aggregated_by_date.index.dtype == 'datetime64[ns]')

    def test_datatypes(self):
        """
        test that all columns in output dataframe have only one type
        """
        test_passed = True
        for col in aggregated_by_date.columns:
            if len(aggregated_by_date[col].map(type).unique()) != 1:
                test_passed = False
                break
        self.assertTrue(test_passed)

    def test_numrows(self):
        """
        check that the number of rows in output dataframe is not equal to zero
        """
        self.assertFalse(aggregated_by_date.shape[0] == 0)

if __name__ == '__main__':
    unittest.main()
