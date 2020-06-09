import unittest
import pandas as pd
import kc_real_estate as kc

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    # Each method in the class to execute a test
    def setUp(self):
        """Defines the data frames and column lists to use for testing."""

        self.kc_data = pd.read_csv('https://raw.githubusercontent.com/' +
                                   'chrico7/data515_project/master/' +
                                   'data515_project/data/kc/' +
                                   'test_kc_data_98122_98144_2016-19.csv',
                                   low_memory=False)

        self.redfin_data = pd.read_csv('https://raw.githubusercontent.com/' +
                                       'chrico7/data515_project/master/' +
                                       'data515_project/data/redfin/' +
                                       'All_King_Redfin.csv',
                                       low_memory=False)

        self.all_data = kc.join_county_redfin(self.kc_data, self.redfin_data)

        self.check_cols = pd.read_csv('https://raw.githubusercontent.com/' +
                                      'chrico7/data515_project/master/' +
                                      'examples/' +
                                      'sample_data_98122_98144_2016-19.csv',
                                      low_memory=False).columns.to_list()

    def test_cols(self):
        """Asserts True if df columns match the expected list check_cols."""

        col_bool = all(elem in self.all_data.columns.to_list() for
                       elem in self.check_cols)

        self.assertTrue(col_bool)


    def test_row(self):
        """Asserts True if there are one or more rows in the dataframe."""

        row_bool = self.all_data.iloc[:1, :].shape[0] >= 1

        self.assertTrue(row_bool)

if __name__ == '__main__':
    unittest.main()
    