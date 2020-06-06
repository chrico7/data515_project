""" Performs King County real estate analysis.

Collects, cleans, aggregates, and visualizes King County real estate data
based on user-defined zip code and time window of interest. Data on the
parcels, buildings, and sales history is from the King County Assessor's
website while data on currently active listings is from the Redfin API.

Functions:

    get_user_input()
    get_county_data()
    get_redfin_data()
    organize_county_data()
    join_county_redfin()
    aggregate_by_zip_spacial()
    zipcode_choro()
    aggregate_by_date()
    trend_plot()

Examples:


"""

# Import packages
import datetime
import difflib
import io
from pathlib import Path
import time
import requests

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define paths
home_path = Path.home()
working_path = Path.cwd() / 'data515_project'
data_path = working_path / 'data'
kc_path = data_path / 'kc'
redfin_path = data_path / 'redfin'
examples_path = working_path / 'examples'
output_path = working_path / 'output'

# Define functions
def get_county_data(file_name, num_rows=None):
    """ Retrieves a single data-file from the King County Assessors webstie.

    Retrieves the single data-file from the King County Assessors webstie
    defined by file_name using the Pandas read_csv() function.

    Args:
        file_name(str): The name of the file to download.
        num_rows(int): The number of rows to return.

    Returns:
        A Pandas dataframe containing all columns of the data retreived from
        the King County Assessor's webstie and number of rows equal to
        num_rows (defaults to all).

    Raises:
        ValueError: If passed file_name is not a string.
        ValueError: If passed file_name is not valid.
        ValueError: If passed num_rows is not a positive integer.
        OSError: If a connection to the URL is unable to be established.
    """

    # Initialize dataframe
    data_raw = pd.DataFrame()

    # Check inputs
    valid_names = ['Accessory', 'Apartment%20Complex', 'Change%20History',
                   'Change%20History%20Detail', 'Commercial%20Building',
                   'Condo%20Complex%20and%20Units',
                   'District%20Levy%20Reference',
                   'Environmental%20Restriction',
                   'Home%20Improvement%20Applications',
                   'Home%20Improvement%20Exemptions', 'Legal', 'Lookup',
                   'Notes', 'Parcel', 'Permit', 'Real%20Property%20Account',
                   'Real%20Property%20Appraisal%20History',
                   'Real%20Property%20Sales', 'Residential%20Building',
                   'Review%20History', 'Tax%20Data', 'Unit%20Breakdown',
                   'Vacant%20Lot', 'Value%20History']

    if not isinstance(file_name, str):
        raise ValueError('Passed file_name must be of type string')

    file_name = file_name.replace(' ', '%20')

    if file_name not in valid_names:
        raise ValueError('The file name you\'ve entered is not valid. ' +
                         'Please check ' +
                         'https://info.kingcounty.gov/assessor/' +
                         'DataDownload/default.aspx for correct file name')

    if num_rows is not None:
        if not isinstance(num_rows, int) & (num_rows > 0):
            raise ValueError('Number or rows to return must be a positive' +
                             f'integer not {num_rows}')

    # Define base URL
    url = f'https://aqua.kingcounty.gov/extranet/assessor/{file_name}.zip'

    # Read in the data
    try:
        data_raw = pd.read_csv(url,
                               nrows=num_rows,
                               low_memory=False)

    except OSError:
        # try three more times with delay
        for i in range(3):
            time.sleep(1)
            try:
                data_raw = pd.read_csv(url,
                                       nrows=num_rows,
                                       low_memory=False)
            except OSError:
                pass
        if data_raw.empty:
            raise OSError('King County Assessor\'s page could not be ' +
                          'reached. Please check that ' +
                          'https://info.kingcounty.gov/assessor/' +
                          'DataDownload/default.aspx is available')

    except UnicodeDecodeError:
        # change encoding to latin-1 in read_csv
        data_raw = pd.read_csv(url,
                               nrows=num_rows,
                               encoding='latin-1',
                               low_memory=False)

    # Check result and return
    if data_raw.shape[0] == 0:
        raise RuntimeError('No data was returned. Please try again later.')

    return data_raw


def get_redfin_data():
    """ Retrieves active King County SFH Redfin listings.

    Retrieves active Redfin listings from either the Redfin API
    or a local file if the API fails. Results are limited to
    single family homes in King County.

    Returns:
        A Pandas dataframe containing all columns of the data retreived from
        the Redfin API or locally stored file.

    Raises:
        OSError: If a connection to the API URL is unable to be established.
        FileNotFoundError: If the local file is not found.
    """

    # Define inner functions
    def get_from_api():
        # Retreives Redfin data using the API

        # Define API URL
        all_king_url = (r'https://www.redfin.com/stingray/api/gis-csv?al=1&' +
                        r'cluster_bounds=-123.04941%2046.84777%' +
                        r'2C-121.01694%2046.84777%2C-121.01694%2047.92442%' +
                        r'2C-123.04941%2047.92442%2C-123.04941%2046.84777&' +
                        r'market=seattle&min_stories=1&num_homes=5000&' +
                        r'ord=redfin-recommended-asc&page_number=1&' +
                        r'region_id=118&region_type=5&sf=1,2,3,5,6,7&' +
                        r'status=1&uipt=1,2,3,4,5,6&v=8')

        # Get API response
        url_data = requests.get(all_king_url).content

        # Check if API response has been blocked
        if "spam bot" in str(url_data):
            raise ValueError("Redfin api error")

        # If API response is not blocked
        redfin_dataframe = pd.read_csv(io.StringIO(url_data.decode('utf-8')))
        if redfin_dataframe.empty:
            raise OSError('The Redfin API page could not be ' +
                          'reached. Please check that ' +
                          'https://redfin.com is available')
        return redfin_dataframe

    def get_from_file():
        # Retreives Redfin data from local file

        file_path = redfin_path / "All_King_Redfin.csv"

        return pd.read_csv(file_path)

    # Retreive Redfin data
    try:
        return get_from_api()
    except ValueError:
        return get_from_file()


def organize_county_data(df_sale, df_building, df_parcel, df_lookup,
                         zip_code: list,
                         start_year='2010', start_month='1', start_day='1',
                         end_year='2020', end_month='1', end_day='1'):
    """ Cleans and organizes data retrieved from King County Assessors website.

    Renames columns consistently, filters data using default and customizable
    inputs, merges data to a single csv file.

    Args:
        df_sale(DataFrame): King County Assessor's sales data
        df_building(DataFrame): King County Assessor's buildings data
        df_parcel(DataFrame): King County Assessor's parcel data
        df_lookup(DataFrame): King County Assessor's lookup data
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

    df_sale = df_sale[df_sale['Major'] != '      ']
    df_sale = df_sale.astype({'Major': int, 'Minor': int})

    #df_lookup_items = pd.read_csv('https://raw.githubusercontent.com/' +
    #                              'chrico7/data515_project/' +
    #                              'master/data/look_up_item.csv')
    #df_col_names = pd.read_csv('https://raw.githubusercontent.com/' +
    #                           'chrico7/data515_project/' +
    #                           'master/data/column_names.csv')

    df_lookup_items = pd.read_csv(data_path / 'look_up_item.csv')
    df_col_names = pd.read_csv(data_path / 'column_names.csv')

    df_sale.columns = (df_col_names[df_col_names['source'] == 'sale'].
                       name.tolist())
    df_building.columns = (df_col_names[df_col_names['source'] == 'building'].
                           name.tolist())
    df_parcel.columns = (df_col_names[df_col_names['source'] == 'parcel'].
                         name.tolist())
    df_lookup.columns = (df_col_names[df_col_names['source'] == 'lookup'].
                         name.tolist())

    df_lookup['Look Up Description'] = (df_lookup['Look Up Description'].
                                        str.strip())

    # get valid zip codes in King County
    kc_zip_codes = df_building['Zip code'].dropna().unique()
    index = []
    for i in range(len(kc_zip_codes)):
        if type(kc_zip_codes[i]) == float:
            kc_zip_codes[i] = int(kc_zip_codes[i])
            kc_zip_codes[i] = str(kc_zip_codes[i])

        if (kc_zip_codes[i][:2] != '98' or (len(kc_zip_codes[i]) != 5 and
                                            len(kc_zip_codes[i]) != 10)):
            index.append(i)

    valid_zip = np.delete(kc_zip_codes, index)

    for i in range(len(valid_zip)):
        if len(valid_zip[i]) == 10:
            valid_zip[i] = valid_zip[i][:5]

    # check zip code(s)
    for code in zip_code:
        if code not in np.unique(valid_zip):
            raise ValueError('The zip code ' + str(code) +
                             ' you\'ve entered is not in King County')

    # check dates
    df_sale['Document Date'] = pd.to_datetime(df_sale['Document Date'])
    start_date = start_year + '-' + start_month + '-' + start_day
    end_date = end_year + '-' + end_month + '-' + end_day

    begin_year = (df_sale.sort_values(['Document Date'], ascending=[True])
                  ['Document Date'].iloc[0].year)
    end_year = (df_sale.sort_values(['Document Date'], ascending=[True])
                ['Document Date'].iloc[-1].year)

    if int(start_year) < int(begin_year):
        raise ValueError('There is no record before year' + str(begin_year))
    if int(start_year) > int(end_year):
        raise ValueError('There is no record after year' + str(end_year))
    if datetime.date(int(start_year), int(start_month), int(start_day)) > \
            datetime.date(int(end_year), int(end_month), int(end_day)):
        raise ValueError('Start date is after end date')

    # clean up the data
    df_building['Zip code'] = pd.to_numeric(df_building['Zip code'],
                                            errors='coerce')
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
    df_sale_sf_recent = df_sale_sf_recent[df_sale_sf_recent['Document Date']
                                          <= end_date]

    # filter by zip code(s)
    df_building_sf_zip = pd.DataFrame()
    for code in zip_code:
        df_building_sf_zip = (df_building_sf_zip.append(
            df_building_sf[df_building_sf['Zip code'] == code]))

    # combine data into a single frame
    new_df = pd.merge(df_building_sf_zip, df_parcel_sf,
                      how='left',
                      left_on=['Major', 'Minor'],
                      right_on=['Major', 'Minor'])

    df_all = pd.merge(new_df, df_sale_sf_recent,
                      how='left',
                      left_on=['Major', 'Minor'],
                      right_on=['Major', 'Minor'])

    # replace numerical codes in records to readable descriptions
    for col in df_all.columns:
        if col in df_lookup_items['Field Name'].tolist():
            look_up_type = int(df_lookup_items[df_lookup_items['Field Name']
                                               == col]['Look Up'])
            look_up_items = df_lookup[df_lookup['Look Up Type']
                                      == look_up_type]

            description_list = []
            for i in range(len(df_all[col])):
                num = df_all[col].iloc[i]
                description = (look_up_items[look_up_items['Look Up Item']
                                             == num]['Look Up Description'])
                if len(description) == 0:
                    description_list.append('nan')
                else:
                    description_list.append(description.values[0])
            df_all[col] = description_list
    return df_all


def join_county_redfin(kc_data, redfin_data):
    """ Joins King County and Redfin data frames based on address mapping.
    Joins the passed dataframes kc_data and redfin_data (representing King
    County and Redfin data respectively) using the pandas merge() function
    and address matching with the difflib get_close_matches() function.
    King County data must contain Major, Minor, Situs Address, and Zip code
    fields. Redfin data must contain MLS#, ADDRESS, and ZIP OR POSTAL CODE
    fields.

    Args:
        kc_data: Dataframe from the King County Assessors office.
                 Must contain Major, Minor, Situs Address, and Zip code fields.
        redfin_data: Dataframe from the Redfin website API.
                     Must contain MLS#, ADDRESS, and ZIP OR POSTAL CODE fields.

    Returns:
        A pandas dataframe containing all fields of both the input kc_data and
        redfin_data dataframes. Data frames are joined on the respective
        address fields with a direct match, or for those without an exact
        match, a fuzzy match as defined by the difflib get_close_matches()
        function.

    Raises:
        ValueError: If passed kc_data is not of type dataframe
        ValueError: If passed redfin_data is not of type dataframe
        ValueError: If passed kc_data is empty
        ValueError: If passed redfin_data is empty
        KeyError: If passed kc_data is missing required columns
        KeyError: If passed redfin_data is missing required columns
    """

    # Initialize dataframe
    data_final = pd.DataFrame()

    # Check inputs
    kc_cols = ['Major', 'Minor', 'Situs Address', 'Zip code']
    redfin_cols = ['MLS#', 'ADDRESS', 'ZIP OR POSTAL CODE']

    # check if dataframe
    if not isinstance(kc_data, pd.DataFrame):
        raise ValueError('Passed kc_data must be of type dataframe')
    if not isinstance(redfin_data, pd.DataFrame):
        raise ValueError('Passed redfin_data must be of type dataframe')

    # check that not empty
    if kc_data.empty:
        raise ValueError('Passed kc_data is empty')
    if redfin_data.empty:
        raise ValueError('Passed redfin_data is empty')

    # check has columns
    if ~pd.Series(kc_cols).isin(kc_data.columns).all():
        raise KeyError('Passed kc_data does not contain required columns:'+
                       'Major, Minor, Situs Address, and Zip code')
    if ~pd.Series(redfin_cols).isin(redfin_data.columns).all():
        raise KeyError('Passed redfin_data does not contain required' +
                       ' columns: Major, Minor, Situs Address, and Zip code')

    # Format data

    # Extract relevant columns
    kc_trim = kc_data[kc_cols].drop_duplicates()
    redfin_trim = redfin_data[redfin_cols].drop_duplicates()

    # Extract list of unique zip_codes
    kc_trim.loc[:, 'Zip code'] = (pd.to_numeric(kc_trim['Zip code'].
                                                fillna('0').str[:5],
                                                errors='coerce').
                                  fillna('0').astype(int))
    zip_codes = (kc_trim.loc[(kc_trim['Zip code'] != 0) &
                             (kc_trim['Zip code'].astype(str).str.len() == 5) &
                             (kc_trim['Zip code'].astype(str).
                              str.contains('^9')),
                             'Zip code'].
                 drop_duplicates().reset_index(drop=True))

    # Replace zip code in Situs Address field
    kc_trim.loc[:, 'Situs Address'] = (kc_trim['Situs Address'].
                                       str.replace('|'.join(zip_codes.
                                                            astype(str).
                                                            to_list()), '')
                                       .str.strip())

    # Trim spaces from Situs Address field
    kc_trim.loc[:, 'Situs Address'] = (kc_trim['Situs Address'].
                                       str.split().str.join(' '))

    # Set both address fields to lowercase
    kc_trim.loc[:, 'Situs Address'] = kc_trim['Situs Address'].str.lower()
    redfin_trim.loc[:, 'ADDRESS'] = redfin_trim['ADDRESS'].str.lower()

    # Drop unit IDs from redfin data address field and insert into position 2
    redfin_trim.loc[:, 'ADDRESS'] = (redfin_trim['ADDRESS'].
                                     where(~(redfin_trim['ADDRESS'].
                                             str.contains('unit', na=False)),
                                           redfin_trim['ADDRESS'].
                                           str.split('unit', 1).str[0]))

    # Join data on exact address matches
    matches_exact = pd.merge(redfin_trim,
                             kc_trim,
                             how='outer',
                             left_on='ADDRESS',
                             right_on='Situs Address')

    # Extract sectors left to match
    redfin_tbd = matches_exact.loc[matches_exact['Situs Address'].isnull(),
                                   redfin_cols].drop_duplicates()

    kc_tbd = matches_exact.loc[(matches_exact['ADDRESS'].isnull())&
                               (matches_exact['Zip code'].
                                isin(redfin_tbd['ZIP OR POSTAL CODE'])),
                               kc_cols].drop_duplicates()

    # Clean matches_exact
    matches_exact = matches_exact[(~matches_exact['ADDRESS'].isnull())&
                                  (~matches_exact['Situs Address'].
                                   isnull())].drop_duplicates()

    # Get fuzzy match on address for each zip code
    matches_fuzzy = pd.DataFrame()
    for zip_code in redfin_tbd['ZIP OR POSTAL CODE'].drop_duplicates():

        # Extract subsets with common zip
        temp_rf = redfin_tbd[redfin_tbd['ZIP OR POSTAL CODE'] ==
                             zip_code].copy()
        temp_kc = kc_tbd[kc_tbd['Zip code'] == zip_code].copy()

        # Extract building number
        temp_rf.loc[:, 'rf_num'] = (temp_rf['ADDRESS'].str.split(' ', 1).
                                    str[0].str.strip())
        temp_kc.loc[:, 'kc_num'] = (temp_kc['Situs Address'].str.split(' ', 1).
                                    str[0].str.strip())

        # Extract street info
        temp_rf.loc[:, 'rf_street'] = (temp_rf['ADDRESS'].str.split(' ', 1).
                                       str[1].str.strip())
        temp_kc.loc[:, 'kc_street'] = (temp_kc['Situs Address'].
                                       str.split(' ', 1).
                                       str[1].str.strip())

        # Add in fuzzy match field
        match_list = temp_kc['kc_street'].drop_duplicates()
        temp_rf.loc[:, 'fuzzy_match'] = (temp_rf['rf_street']
                                         .map(lambda x:
                                              difflib.get_close_matches(str(x),
                                                                        match_list,
                                                                        n=1,
                                                                        cutoff=0.6))).str.join(',')

        # Merge on building number and fuzzy match
        temp_all = pd.merge(temp_kc,
                            temp_rf,
                            how='inner',
                            left_on=['kc_num', 'kc_street'],
                            right_on=['rf_num', 'fuzzy_match'])

        # Drop cols
        temp_all = temp_all.drop(['rf_num', 'rf_street',
                                  'fuzzy_match',
                                  'kc_num', 'kc_street'], axis=1)

        # Append to frame
        matches_fuzzy = matches_fuzzy.append(temp_all)

    # Combine matches
    matches_all = pd.concat([matches_exact, matches_fuzzy])

    # Extract join fields
    match_fields = (matches_all[['MLS#', 'Major', 'Minor']].
                    drop_duplicates())

    # Join kc and redfin data
    data_final = pd.merge(kc_data,
                          match_fields,
                          how='left', on=['Major', 'Minor'])

    data_final = pd.merge(data_final,
                          redfin_data,
                          how='left', on=['MLS#'])

    return data_final

####
## Run Module
####
"""
# Get raw assessor's data
print("Thanks for using the King County Real Estate Tool! \n" +
      "Hold on, we're getting the most recent historical data "+
      "from the King County Assessor and current active " +
      "listings from Redfin")

df_sale = get_county_data("Real%20Property%20Sales")
df_building = get_county_data("Residential%20Building")
df_parcel = get_county_data("Parcel")
df_lookup = get_county_data("Lookup")

# Get raw redfin data
df_redfin = get_redfin_data()

# get user input and generate variables
if __name__ == "__main__":

    # Ask if user would like to use defaults
    while True:
        use_default = (input("Would you like to use" +
                             "tool defaults? (Yes/No): "))

        # Check inputs
        try:
            isinstance(use_default, bool)
        except ValueError:
            print("Please enter True or False!")
        else:
            break

    # Define tool parameters (user input or default)
    if use_default:
        zip_code = ['98122', '98144']
        start_year = '2016'
        start_month = '1'
        start_day = '1'
        end_year = '2019'
        end_month = '12'
        end_day = '31'
    else:
        zip_code = [str(item) for item in input("Enter zip code " +
                                                "(separated by comma) : ").
                    split()]
        start_year = (input("Enter start year: "))
        start_month = (input("Enter start month: "))
        start_day = (input("Enter start day: "))
        end_year = (input("Enter end year: "))
        end_month = (input("Enter end month: "))
        end_day = (input("Enter end day: "))

# Organize King County data
df_county = organize_county_data(df_sale, df_building, df_parcel, df_lookup,
                                 zip_code,
                                 start_year, start_month, start_day,
                                 end_year, end_month, end_day)

# Combine assessor and redfin data
all_data = join_county_redfin(df_county, df_redfin)
"""
# Generate visualizations from resulting dataframes, aggregating for easy charting

def aggregate_by_zip_spacial(input_dataframe=
                             pd.read_csv(examples_path /
                                         "sample_data_98075_2018-19.csv")):
    """
    Aggregates a joined input dataframe by date to allow easy graphing of trends

    Args:
        input_dataframe: an input dataframe of a format consistent with the output of
        the local join_county_redfin() function. If no input is provided, then the
        default example dataframe is used.

    Returns:
        A Pandas dataframe aggregating key columns of interest within the dataframe.

    Raises:
        KeyError: If passed input_dataframe is missing required columns
    """
    # defined required columns for aggregation
    required_cols = ['Document Date', 'LONGITUDE', 'LATITUDE', 'PRICE',
                     'DAYS ON MARKET', 'SQUARE FEET', '$/SQUARE FEET']

    # check has required columns
    if ~pd.Series(required_cols).isin(input_dataframe.columns).all():
        raise KeyError('Passed input data does not contain required columns:'+
                       'Document Date, LONGITUDE, LATITUDE, PRICE' +
                       'DAYS ON MARKET, SQUARE FEET and $/SQUARE FEET')

    #convert kc date column to dates
    input_dataframe['Document Date'] = input_dataframe['Document Date'].astype('datetime64[ns]')

    #convert to geodataframe for easy merging
    input_dataframe = gpd.GeoDataFrame(input_dataframe,
                                       geometry=gpd.points_from_xy(input_dataframe['LONGITUDE'],
                                                                   input_dataframe['LATITUDE']))

    #pull in King County zip shapefiles and pare down to geometry and zip
    df_zip_shape = gpd.read_file(
        "https://opendata.arcgis.com/datasets/06da0f67fc1948e3aae93063750ad02b_790.geojson")
    df_zip_shape = df_zip_shape[['ZIP', 'geometry']]

    #aggregate meaningful redfin variables
    input_dataframe = gpd.sjoin(df_zip_shape,
                                input_dataframe).groupby("Zip code").agg({'PRICE':'mean',
                                                                          'DAYS ON MARKET':'mean',
                                                                          'SQUARE FEET':'mean',
                                                                          '$/SQUARE FEET':'mean'})

    #rename columns to reflect aggregation
    input_dataframe.columns = ['Mean sale price',
                               'Mean days on market',
                               'Mean size (square feet)',
                               'Mean cost per sqft']

    #merge aggregated redfin with with zip dataframe
    merged_df = df_zip_shape.merge(input_dataframe, left_on='ZIP', right_on='Zip code')

    return merged_df

def zipcode_choro(opening_data=aggregate_by_zip_spacial(), mapping_var='Mean sale price'):
    """
    Creates a simple zipcode choropleth map for the variable of interest

    Args:
        input_dataframe: aggregated dataframe of a format consistent with the output of
        aggregate_by_zip_spacial.If no input is provided, the default example dataframe
        from that function is used.

        mapping_var: a string identifying the varuable to be mapped; must be a column name
        within input_dataframe.

    Returns:
        A saved png of the matplotlib object mapping the variable of interest by zipcode
        in King County.

    Raises:
        ValueError: If passed mapping_var is not a column within input_dataframe.
        ValueError: If passed input_dataframe does not have 2 or more zipcodes to map
    """
    # check that mapping_var is within input_dataframe
    if mapping_var not in opening_data.columns:
        raise ValueError('The mapping variable that you\'ve entered is not valid. ' +
                         'Please select a column from your input dataframe (below)' +
                         'or select a new input dataframe.')

    # check that at least two zipcodes to map within input_dataframe
    if len(np.unique(opening_data['ZIP'])) < 2:
        raise ValueError('The input dataframe has fewer than two zipcodes - please'+
                         ' expand the dataframe to produce a meaningful map.')

    #create a basic matplotlib figure
    ch_fig, ch_ax = plt.subplots(1)
    opening_data.plot(column=mapping_var, ax=ch_ax, linewidth=0.5, edgecolor='0.5',
                      legend=True)
    ch_ax.set_axis_off()
    plt.axis('equal')
    plt.title(mapping_var)
    plt.savefig(output_path / 'zipcode_choro_output.png')

def aggregate_by_date(input_dataframe=pd.read_csv(examples_path /
                                                  "sample_data_98075_2018-19.csv")):
    """
    Aggregates a joined input dataframe by date to allow easy graphing of trends

    Args:
        input_dataframe: an input dataframe of a format consistent with the output of [func].
        If no input is provided, the default example dataframe is used
    Returns:
        A Pandas dataframe aggregating key columns [ ]
    Raises:
        ValueError: If passed file_name is not a string.
        ValueError: If passed file_name is not valid.
        ValueError: If passed num_rows is not a positive integer.
        OSError: If a connection to the URL is unable to be established.
    """
    #convert county transaction date to datetime format
    input_dataframe['Document Date'] = input_dataframe['Document Date'].astype('datetime64[ns]')

    #aggregate key variables in dataframe by date
    input_aggregate = input_dataframe.groupby(["Document Date"]).agg(
        {'Sale Price':'mean',
         'Excise Tax Number':'nunique'})

    #rename columns to reflect aggregation
    input_aggregate.columns = ['Mean sale price', 'Number of transactions']

    #remove any miscodes (some dates in 2070)
    input_aggregate = input_aggregate[input_aggregate.index < datetime.datetime.now()]
    return input_aggregate

def trend_plot(input_dataframe=aggregate_by_date(), trend_variable='Mean sale price'):
    """
    Creates a simple matplotlib line graph of the variable of interest

    Args:
        input_dataframe: an input dataframe of a format consistent with the output of
        aggregate_by_date. If no input is provided, then the default example
        dataframe is used.

        trend_variable: an input string specifying the variable of interest. If no input is
        provided then mean sale price is graphed.
    Returns:
        A saved png of the matplotlib line graph object

    """
    #create simple figure
    #fig = plt.figure()
    plt.rcParams["figure.figsize"] = (10, 10)
    tr_ax = plt.axes()
    tr_x = input_dataframe.index
    tr_y = input_dataframe[trend_variable]
    tr_ax.plot(tr_x, tr_y)
    plt.title(trend_variable)
    tr_ax.set_xlim([min(input_dataframe.index), max(input_dataframe.index)])
    plt.savefig(output_path / 'trend_plot_output.png')
