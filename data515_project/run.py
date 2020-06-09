"""module runs data import features of the tool.
Contains a single function:
lets_begin()
"""

from data515_project.kc_real_estate import *

# Get raw assessor's data
print("Thank you for using the King County Real Estate Tool! \n" +
      "Hold on, we're getting the most recent historical data "+
      "from the King County Assessor and current active " +
      "listings from Redfin. We will let you know when the data " +
      "is collected.")

df_sale = get_county_data("Real%20Property%20Sales")
df_building = get_county_data("Residential%20Building")
df_parcel = get_county_data("Parcel")
df_lookup = get_county_data("Lookup")

# Get raw redfin data
df_redfin = get_redfin_data()

print("Data is collected. To explore Redfin's King County MLS " +
      "Data run kc.view_redfin_data_by_price(kc.df_redfin) " +
      "below. Or to begin querying the data run kc.lets_begin()" +
      " in the cell below.")

####
## Query Data By Zip and Date
####
def lets_begin():
    """ Begins the data query based on user inputted data. This function allows the user
        to easily query the data by zip_code and date

    Args:
        None

    Returns:
        A Pandas DataFrame

    Raises:
        KeyError: If the user doesn't input 'Yes' or No'
    """
    # get user input and generate variables
    while True:
        user_input = (input("Would you like to use" +
                            "tool defaults? (Yes/No): "))

        # Check inputs
        if user_input != "Yes" and user_input != "No":
            print("Please enter Yes or No")
        else:
            break

    # Define tool parameters (user input or default)
    if user_input == 'Yes':
        zip_code = ['98122', '98144', '98103', '98039']
        start_year = '2018'
        start_month = '1'
        start_day = '1'
        end_year = '2019'
        end_month = '12'
        end_day = '31'
    else:
        zip_code = [x.strip(' ') for x in
                    input("Enter zip code (separated by comma) : ").split(',')]
        #print(zip_code)
        start_year = (input("Enter start year: "))
        start_month = (input("Enter start month: "))
        start_day = (input("Enter start day: "))
        end_year = (input("Enter end year: "))
        end_month = (input("Enter end month: "))
        end_day = (input("Enter end day: "))

    print("Querying King County Data")
    # Organize King County data
    df_county = organize_county_data(df_sale, df_building, df_parcel, df_lookup,
                                     zip_code,
                                     start_year, start_month, start_day,
                                     end_year, end_month, end_day)
    print("Joining with Redfin Data")

    # Combine assessor and redfin data
    result = join_county_redfin(df_county, df_redfin)
    return result
