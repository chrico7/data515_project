from get_county_data import *
import pandas as pd
import numpy as np
import datetime


def filter_county_data(zip_code: list, start_year='2010', start_month='1', start_day='1',
                       end_year='2020', end_month='1', end_day='1', is_test = False):
    """ Cleans and organizes data retrieved from the King County Assessors website.

    Renames columns consistently, filters data using default and customizable inputs,
    merges data to a single csv file.

    Args:
        zip_code(list): List of zip codes in the King County.
        start_year(str): Include property sale data from this year.
        start_month(str): Include property sale data from this month.
        start_day(str): Include property sale data from this day.
        end_year(str): Include property sale data to this year.
        end_month(str): Include property sale data to this month.
        end_day(str): Include property sale data to this day.

    Returns:
        A Pandas dataframe containing all the data retrieved from
        the King County Assessor's website, filtered and merged.

    Raises:
        ValueError: If passed zip code is not valid.
        ValueError: If passed start_year is before the first record.
        ValueError: If passed end_year is after the last record.
        ValueError: If start date is after end date based on passed values.
    """

    if is_test:
        # import data from local is doing unit tests
        df_sale = pd.read_csv('./test_data/sale.csv', encoding='latin-1', low_memory=False)
        df_building = pd.read_csv('./test_data/building.csv', encoding='latin-1', low_memory=False)
        df_parcel = pd.read_csv('./test_data/parcel.csv', encoding='latin-1', low_memory=False)
        df_lookup = pd.read_csv('./test_data/EXTR_LookUp.csv', encoding='latin-1', low_memory=False)
    else:
        # get data using get_county_data()
        df_sale = get_county_data("Real%20Property%20Sales")
        df_building = get_county_data("Residential%20Building")
        df_parcel = get_county_data("Parcel")
        df_lookup = get_county_data("Lookup")

    df_lookup_items = pd.read_csv('../data/look_up_item.csv')
    df_col_names = pd.read_csv('../data/column_names.csv')

    df_sale.columns = df_col_names[df_col_names['source'] == 'sale'].name.tolist()
    df_building.columns = df_col_names[df_col_names['source'] == 'building'].name.tolist()
    df_parcel.columns = df_col_names[df_col_names['source'] == 'parcel'].name.tolist()
    df_lookup.columns = df_col_names[df_col_names['source'] == 'lookup'].name.tolist()

    df_lookup['Look Up Description'] = df_lookup['Look Up Description'].str.strip()

    df_sale = df_sale[df_sale['Major'] != '      ']
    df_sale = df_sale.astype({'Major': int, 'Minor': int})

    # get valid zip codes in King County
    kc_zip_codes = df_building['Zip code'].dropna().unique().tolist()
    index = []
    for i in range(len(kc_zip_codes)):

        if type(kc_zip_codes[i]) == float or type(kc_zip_codes[i] == int):
            kc_zip_codes[i] = int(kc_zip_codes[i])
            kc_zip_codes[i] = str(kc_zip_codes[i])
        if kc_zip_codes[i][:2] != '98' or (len(kc_zip_codes[i]) != 5 and len(kc_zip_codes[i]) != 10):
            index.append(i)
    valid_zip = np.delete(kc_zip_codes, index)
    for i in range(len(valid_zip)):
        if len(valid_zip[i]) == 10:
            valid_zip[i] = valid_zip[i][:5]

    # check zip code(s)
    for code in zip_code:
        if code not in np.unique(valid_zip):
            raise ValueError('The zip code ' + str(code) + ' you\'ve entered is not in King County')

    # check dates
    df_sale['Document Date'] = pd.to_datetime(df_sale['Document Date'])
    start_date = start_year + '-' + start_month + '-' + start_day
    end_date = end_year + '-' + end_month + '-' + end_day

    begin_year = df_sale.sort_values(['Document Date'], ascending=[True])['Document Date'].iloc[0].year
    end_year = df_sale.sort_values(['Document Date'], ascending=[True])['Document Date'].iloc[-1].year

    if int(start_year) < int(begin_year):
        raise ValueError('There is no record before year' + str(begin_year))
    if int(start_year) > int(end_year):
        raise ValueError('There is no record after year' + str(end_year))
    if datetime.date(int(start_year), int(start_month), int(start_day)) > \
            datetime.date(int(end_year), int(end_month), int(end_day)):
        raise ValueError('Start date is after end date')

    # clean up the data
    df_building['Zip code'] = pd.to_numeric(df_building['Zip code'], errors='coerce')
    df_building = df_building.dropna(subset=['Zip code'])
    df_building['Zip code'] = df_building['Zip code'].astype(int)
    df_building['Zip code'] = df_building['Zip code'].astype(str)

    # limit properties to only single family houses
    df_parcel_sf = df_parcel[df_parcel['Property Type'] == 'R']
    df_parcel_sf = df_parcel_sf.drop(columns=['Property Type'])
    df_sale_sf = df_sale[df_sale['Property Type'] == 11]
    df_building_sf = df_building[df_building['Number Living Units'] == 1]

    # filter by a start date and end date
    df_sale_sf_recent = df_sale_sf[df_sale_sf['Document Date'] >= start_date]
    df_sale_sf_recent = df_sale_sf_recent[df_sale_sf_recent['Document Date'] <= end_date]

    # filter by zip code(s)
    df_building_sf_zip = pd.DataFrame()
    for code in zip_code:
        df_building_sf_zip = df_building_sf_zip.append(df_building_sf[df_building_sf['Zip code'] == code])

    new_df = pd.merge(df_building_sf_zip, df_sale_sf_recent, how='left', left_on=['Major', 'Minor'],
                      right_on=['Major', 'Minor'])
    df_all = pd.merge(new_df, df_parcel_sf, how='left', left_on=['Major', 'Minor'], right_on=['Major', 'Minor'])

    # replace numerical codes in records to readable descriptions
    for col in df_all.columns:
        if col in df_lookup_items['Field Name'].tolist():
            look_up_type = int(df_lookup_items[df_lookup_items['Field Name'] == col]['Look Up'])
            look_up_items = df_lookup[df_lookup['Look Up Type'] == look_up_type]
            description_list = []
            for i in range(len(df_all[col])):
                num = df_all[col].iloc[i]
                description = look_up_items[look_up_items['Look Up Item'] == num]['Look Up Description']
                if len(description) == 0:
                    description_list.append('nan')
                else:
                    description_list.append(description.values[0])
            df_all[col] = description_list
    return df_all


if __name__ == "__main__":
    zip_code = [str(item) for item in input("Enter zip code (separated by comma) : ").split()]
    start_year = (input("Enter start year: "))
    start_month = (input("Enter start month: "))
    start_day = (input("Enter start day: "))
    end_year = (input("Enter end year: "))
    end_month = (input("Enter end month: "))
    end_day = (input("Enter end day: "))
    filter_county_data(zip_code, start_year, start_month, start_day, end_year, end_month, end_day)
