import sys
import unittest
from datetime import datetime

sys.path.insert(1, '../../code')
from data515_project.kc_real_estate import organize_county_data

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    # Each method in the class to execute a test
    def setUp(self):
        """Defines the data frames and column lists to use for testing."""

        self.df_kc = organize_county_data(['98136', '98108', '98115', '98133', '98038'],
                                           start_year='2000', start_month='1', start_day='1',
                                           end_year='2020', end_month='1', end_day='1', is_test=True)
        self.check_zip = ['98136', '98108', '98115', '98133', '98038']
        self.check_start_date = datetime.strptime('01/01/00', "%m/%d/%y")
        self.check_end_date = datetime.strptime('01/01/20', "%m/%d/%y")
        self.property_type = 'Household, single family units'
        self.living_unit = 1

    def test_zips(self):
        """Asserts True if the returned dataframe contains properties in the correct zip code(s)."""

        self.assertTrue(all(elem in self.df_kc['Zip code'].unique().tolist() for
                            elem in self.check_zip))

    def test_dates(self):
        """Asserts True if the returned dataframe contains sale records in the correct time frame."""
        self.df_sorted_by_date = self.df_kc.sort_values(by='Document Date', ascending=True)
        self.df_start_date = datetime.strptime(
            str(self.df_sorted_by_date[self.df_sorted_by_date['Document Date'].notna()]['Document Date'].iloc[0]),
            "%Y-%m-%d %H:%M:%S")
        self.df_end_date = datetime.strptime(
            str(self.df_sorted_by_date[self.df_sorted_by_date['Document Date'].notna()]['Document Date'].iloc[-1]),
            "%Y-%m-%d %H:%M:%S")

        start_bool = self.df_start_date >= self.check_start_date
        end_bool = self.df_end_date <= self.check_end_date

        self.assertTrue(start_bool and end_bool)

    def test_property(self):
        """Asserts True if the returned dataframe contains the correct property type (single family houses)"""
        property_bool = self.df_kc['Property Type'][self.df_kc['Property Type'] != 'nan'].unique()[0] == \
                        self.property_type

        unit_bool = self.df_kc['Number Living Units'][self.df_kc['Number Living Units'].notna()].unique()[0] == \
                    self.living_unit

        self.assertTrue(property_bool and unit_bool)


if __name__ == '__main__':
    unittest.main()
