import unittest
import kc_real_estate as kc

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    # Each method in the class to execute a test
    def setUp(self):
        """Defines the data frames and column lists to use for testing."""

        self.df_sale = kc.get_county_data("Real%20Property%20Sales")
        self.df_building = kc.get_county_data("Residential%20Building")
        self.df_parcel = kc.get_county_data("Parcel")

        self.check_cols_sale = ['Major', 'Minor',
                                'DocumentDate', 'PropertyType']
        self.check_cols_building = ['Major', 'Minor',
                                    'Address', 'ZipCode',
                                    'NbrLivingUnits']
        self.check_cols_parcel = ['Major', 'Minor',
                                  'PropType']

    def test_cols(self):
        """Asserts True if dataframe columns match list check_cols."""

        sale_col_bool = all(elem in self.df_sale.columns.to_list() for
                            elem in self.check_cols_sale)
        building_col_bool = all(elem in self.df_building.columns.to_list() for
                                elem in self.check_cols_building)
        parcel_col_bool = all(elem in self.df_parcel.columns.to_list() for
                              elem in self.check_cols_parcel)

        self.assertTrue(sale_col_bool and
                        building_col_bool and
                        parcel_col_bool)


    def test_row(self):
        """Asserts True if there are one or more rows in each dataframe."""

        sale_row_bool = self.df_sale.iloc[:1, :].shape[0] >= 1
        building_row_bool = self.df_building.iloc[:1, :].shape[0] >= 1
        parcel_row_bool = self.df_parcel.iloc[:1, :].shape[0] >= 1

        self.assertTrue(sale_row_bool and
                        building_row_bool and
                        parcel_row_bool)

if __name__ == '__main__':
    unittest.main()
    
