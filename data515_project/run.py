from data515_project.kc_real_estate import *

####
## Run Module
####

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

print("Data is collected. To begin run kc.lets_begin() in the cell below.")


def lets_begin():
    # get user input and generate variables
    while True:
        user_input = (input("Would you like to use" +
                             "tool defaults? (Yes/No): "))
        
        # Check inputs
        if user_input != "Yes" and user_input !="No":
            print("Please enter Yes or No")
        else:
            break

    # Define tool parameters (user input or default)
    if user_input == 'Yes':
        zip_code = ['98122', '98144']
        start_year = '2016'
        start_month = '1'
        start_day = '1'
        end_year = '2019'
        end_month = '12'
        end_day = '31'
    else:
        zip_code = [str(item) for item in input("Enter zip code " +
                                                "(separated by comma) : ").split()]
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
    all_data = join_county_redfin(df_county, df_redfin)
    return all_data