import unittest
import kc_real_estate as kc

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    # Each method in the class to execute a test
    def setUp(self):
        """Defines the data frames and column lists to use for testing."""

        self.df_redfin = kc.get_redfin_data()
        self.check_cols = ['SALE TYPE', 'SOLD DATE', 'PROPERTY TYPE',
                           'ADDRESS', 'CITY', 'STATE OR PROVINCE',
                           'ZIP OR POSTAL CODE', 'PRICE', 'BEDS', 'BATHS',
                           'LOCATION', 'SQUARE FEET', 'LOT SIZE',
                           'YEAR BUILT', 'DAYS ON MARKET', '$/SQUARE FEET',
                           'HOA/MONTH', 'STATUS', 'SOURCE', 'MLS#',
                           'FAVORITE', 'INTERESTED', 'LATITUDE', 'LONGITUDE']

    def test_cols(self):
        """Asserts True if df columns exactly match expected list check_cols."""

        col_bool = all(elem in self.df_redfin.columns.to_list()
                       for elem in self.check_cols)

        self.assertTrue(col_bool)


    def test_row(self):
        """Asserts True if there are one or more rows in the dataframe."""

        row_bool = self.df_redfin.iloc[:1, :].shape[0] >= 1

        self.assertTrue(row_bool)

if __name__ == '__main__':
    unittest.main()
    