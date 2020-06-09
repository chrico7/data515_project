"""
Unit test for named function
"""
import unittest
from data515_project.kc_real_estate import aggregate_by_zip_spacial

aggregated_by_zip = aggregate_by_zip_spacial()
aggregated_by_zip_cols = aggregated_by_zip.columns

# Define a class in which the tests will run
class TestAggByZip(unittest.TestCase):
    """
    This implements the three test methods below.

    """

    # Each method in the class to execute a test
    def test_zipcodes(self):
        """
        test that function output dataframe has a zipcode column
        which is necessary for the primary use of the function
        """
        self.assertTrue("Zip code" in aggregated_by_zip_cols)

    def test_numrows(self):
        """
        check that the number of rows in output dataframe is not equal to zero
        """
        self.assertFalse(aggregated_by_zip.shape[0] == 0)

if __name__ == '__main__':
    unittest.main()
