# Functional Requirements  

## Background  

Buying a home is the largest single purchase that most people will make in their entire lives.<sup>1</sup> Additionally, the residential real estate market is one of the largest components of the American economy.<sup>2</sup> Despite this prominence, good data on real estate trends and transactions is almost impossible to find due to two main limitations: first, real estate transactions are recorded at the county level with a wide variation in the definitions, practices, and reporting standards for each transaction. Second, most real estate transactions are conducted with the assistance of a licensed realtor and their associated Multiple Listing Service (MLS) that treats all transaction data as proprietary. These two factors together have resulted in a real estate data landscape that is fragmented, inconsistent, and difficult to access for the individual consumer that is attempting to buy or sell real estate.  

Our project attempts to mitigate these difficulties by creating a tool to collect real estate listing and transaction data for Seattle, WA from the King County Assessor’s office and real estate brokerage firm Redfin. This data can then be used to feed tools to better inform individual consumers on the current state of the real estate market in general or specific properties of interest. 

## User Profile  

The intended users of our final product are individuals interested in buying or selling real estate in Seattle, with sector knowledge of real estate and analytic skills, but do not have experience or knowledge of the administrative terms used by the King County Assessor or the ability to manipulate and parse the large data files available on the Assessor’s website.  

Basic users should be able to interact with simple online interactive maps and dashboards. Intermediate users should be comfortable with basic data analysis using tools such as Excel. Advanced users should be able to clone a git repository and run a Python script.  

## Data Sources  

The data of interest is split across listing records and transaction records. Listing records, usually the purview of the local MLSs, records the history of the property’s time on the market. This includes the initial list price, time on the market, and any history of price reductions or failed transactions. Transaction records, maintained by the Assessor’s office for each county, define the terms of the final transaction as recorded on the legal record of transaction (deed). Our project will utilize transaction data from the King County Assessor’s office as well as listing data from the online real estate brokerage Redfin.  

__King County Assessor's Data__  
https://info.kingcounty.gov/assessor/DataDownload/default.aspx

The King County Assessor makes freely available (for non-commercial use) extracts from its property assessment database. The data describes the characteristics and assessed value of housing in the county, as well as all sales transactions of real estate registered with the Assessor.  

__Redfin Active Listings__   
https://www.redfin.com/blog/data-center/

Redfin is a real estate brokerage firm with a sophisticated web interface that displays currently active listings in a given geographic area. Additionally, data download is supported with proper citation and for non-commercial purposes. A description of the data is available [here](https://docs.google.com/spreadsheets/d/1YNT5VfZTwSnUK7nqGAPGZUqOVBbsIC_M1vTgYCCLtVg/edit#gid=635767466). Each week they release a dataset of trends in the housing market by region.  

## Use Cases  

__Use Case 1:__  
User wants independent guidance on an appropriate listing price of their house.

- User: Inputs zipcode of interest   
    - Tool:  retrieves latest listings data for zipcode of interest
    - Tool:  retrieves latest assessor's’ data for zipcode of interest
    - Tool:  merges two data sources and creates aggregations

- User: Selects variables of interest and creates plots of interest
   - Tool: takes user selection of variables of interest
   - Tool: filters merged data
   - Tool: produces visualizations of selected variables

    
__Use Case 2:__  
User is researching neighborhoods in Seattle for making investment.

- User: Select zip-code/s and time span
   - Tool: retrieves latest assessor's’ data for zipcode of interest
   - Tool: pull and process data based on parameters from the UI Manager and send to the Figure Manager
   - User: Rank neighborhood by selling/listing price ratio

- User: Select metric for comparison
    - Tool: display data trends for selected zip codes
    - Tool: generate plots showing data trends

1: “More people are buying a home — the biggest financial decision of their lives — sight unseen”,  
    Seattle Times, 20 July 2018 [link](https://www.seattletimes.com/business/real-estate/more-people-are-buying-a-home-the-biggest-financial-decision-of-their-lives-sight-unseen/)  
    
2: See for example Congressional Research Service report: Introduction to U.S. Economy: Housing Market (October 2019)  
    https://fas.org/sgimes p/crs/misc/IF11327.pdf
