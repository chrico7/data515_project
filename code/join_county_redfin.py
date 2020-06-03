def join_county_redfin(kc_data, redfin_data):
    """ Joins King County and Redfin data frames based on address mapping.

    Joins the passed dataframes kc_data and redfin_data (representing King
    County and Redfin data respectively) using the pandas merge() function
    and address matching with the difflib get_close_matches() function.
    King County data must contain Major, Minor, Address, and ZipCode fields.
    Redfin data must contain MLS#, ADDRESS, and ZIP OR POSTAL CODE fields.

    Args:
        kc_data: Dataframe from the King County Assessors office.
                 Must contain Major, Minor, Address, and ZipCode fields.
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

    # Import packages DELETE THIS LATER
    import pandas as pd
    import difflib

    # Initialize dataframe
    data_final = pd.DataFrame()

    # Check inputs
    kc_cols = ['Major', 'Minor', 'Address', 'ZipCode']
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
                       'Major, Minor, Address, and ZipCode')
    if ~pd.Series(redfin_cols).isin(redfin_data.columns).all():
        raise KeyError('Passed redfin_data does not contain required' +
                       ' columns: Major, Minor, Address, and ZipCode')

    # Format data

    # Extract relevant columns
    kc_trim = kc_data[kc_cols].drop_duplicates()
    redfin_trim = redfin_data[redfin_cols].drop_duplicates()

    # Extract list of unique zip_codes
    kc_trim.loc[:, 'ZipCode'] = (pd.to_numeric(kc_trim['ZipCode'].
                                               fillna('0').str[:5],
                                               errors='coerce').
                                 fillna('0').astype(int))
    zip_codes = kc_trim.loc[(kc_trim['ZipCode'] !=0 ) &
                            (kc_trim['ZipCode'].astype(str).str.len() == 5) &
                            (kc_trim['ZipCode'].astype(str).str.contains('^9')),
                            'ZipCode'].drop_duplicates().reset_index(drop=True)

    # Replace zip code in Address field
    kc_trim.loc[:, 'Address'] = (kc_trim['Address'].
                                 str.replace('|'.join(zip_codes.
                                                      astype(str).
                                                      to_list()), '')
                                 .str.strip())

    # Trim spaces from Address field
    kc_trim.loc[:, 'Address'] = kc_trim['Address'].str.split().str.join(' ')

    # Set both address fields to lowercase
    kc_trim.loc[:, 'Address'] = kc_trim['Address'].str.lower()
    redfin_trim.loc[:, 'ADDRESS'] = redfin_trim['ADDRESS'].str.lower()

    # Drop unit IDs from redfin data address field and insert into position 2
    redfin_trim.loc[:, 'ADDRESS'] = (redfin_trim['ADDRESS'].
                                     where(~redfin_trim['ADDRESS'].
                                           str.contains('unit'),
                                           redfin_trim['ADDRESS'].
                                           str.split('unit', 1).str[0]))

    # Join data on exact address matches
    matches_exact = pd.merge(redfin_trim,
                             kc_trim,
                             how='outer',
                             left_on='ADDRESS',
                             right_on='Address')

    # Extract sectors left to match
    redfin_tbd = matches_exact.loc[matches_exact['Address'].isnull(),
                                   redfin_cols].drop_duplicates()

    kc_tbd = matches_exact.loc[(matches_exact['ADDRESS'].isnull())&
                               (matches_exact['ZipCode'].
                                isin(redfin_tbd['ZIP OR POSTAL CODE'])),
                               kc_cols].drop_duplicates()

    # Clean matches_exact
    matches_exact = matches_exact[(~matches_exact['ADDRESS'].isnull())&
                                  (~matches_exact['Address'].isnull())].drop_duplicates()

    # Get fuzzy match on address for each zip code
    matches_fuzzy = pd.DataFrame()
    for zip_code in redfin_tbd['ZIP OR POSTAL CODE'].drop_duplicates():

        # Extract subsets with common zip
        temp_rf = redfin_tbd[redfin_tbd['ZIP OR POSTAL CODE'] == zip_code].copy()
        temp_kc = kc_tbd[kc_tbd['ZipCode'] == zip_code].copy()

        # Extract building number
        temp_rf.loc[:, 'rf_num'] = (temp_rf['ADDRESS'].str.split(' ', 1).
                                    str[0].str.strip())
        temp_kc.loc[:, 'kc_num'] = (temp_kc['Address'].str.split(' ', 1).
                                    str[0].str.strip())

        # Extract street info
        temp_rf.loc[:, 'rf_street'] = (temp_rf['ADDRESS'].str.split(' ', 1).
                                      str[1].str.strip())
        temp_kc.loc[:, 'kc_street'] = (temp_kc['Address'].str.split(' ', 1).
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
        temp_all = pd.merge(temp_rf,
                            temp_kc,
                            how='inner',
                            left_on=['rf_num', 'fuzzy_match'],
                            right_on=['kc_num', 'kc_street'])
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
                    drop_duplicates().astype(int))

    # Join kc and redfin data
    data_final = pd.merge(redfin_data,
                          match_fields,
                          how='left', on=['MLS#'])
    data_final = pd.merge(data_final,
                          kc_data,
                          how='left', on=['Major', 'Minor'])

    return data_final
