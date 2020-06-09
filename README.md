[![Build Status](https://travis-ci.org/chrico7/data515_project.svg?branch=master)](https://travis-ci.org/chrico7/data515_project)
# King County Real Estate Visualization Tool
----
Final project for DATA515 spring 2020

Buying a home is the largest single purchase that most people will make in their entire lives<sup>1</sup>. Additionally, the residential real estate market is one of the largest components of the American economy<sup>2</sup> and is closely regulated. Even so, good data on real estate trends and transactions is difficult to find and to access.

We address this problem locally with a tool that collects, cleans, joins and visualizes real estate administrative and listing data.

----

## Team members
Corey Christopherson<br/>
Richard Todd<br/>
Maggie Weatherly<br/>
Ruian Yang

## Data
- [Source 1: Redfin](https://www.redfin.com)

- [Source 2: King County Department of Assessments](https://info.kingcounty.gov/assessor/DataDownload/default.aspx)

- [Source 3: King County GIS Open Data](https://gis-kingcounty.opendata.arcgis.com/datasets/e6c555c6ae7542b2bdec92485892b6e6_113)

## Modules

### kc_real_estate.py
This contains the following functions, which form the core of the tool's operation:
- get_user_input()
- get_county_data()
- get_redfin_data()
- organize_county_data()
- join_county_redfin()
- aggregate_by_zip_spacial()
- zipcode_choro()
- aggregate_by_date()
- trend_plot()
- plotly_by_date()
- zip_code_agg_plotly()
- view_redfin_data_by_agg()

### run.py
This contains a single function - lets_begin() - which is used in the setup and data load of the tool (see below).

## Software dependencies and license information

#### Programming language: 

- Python version 3.0 and above 

#### Packages:

- NumPy 1.11.1  
- pandas 1.0.4  
- matplotlib 1.5.3  
- geopanda 0.7.0 
- ipywidgets 7.5.1 
- requests 2.23.0
- plotly 4.8.1
- notebook 6.0.3

#### Installation:

We recommend using conda to manage your python environment and packages

$ git clone https://github.com/chrico7/data515_project.git
$ cd data515_project/
$ conda install --file requirements.txt
$ python3 setup.py install
$ jupyter notebook

Then run <code>import data515_project.run as kc</code>. See Demo.ipynb for examples.

#### Licensing info:

The MIT License is a permissive free software license originating at the Massachusetts Institute of Technology (MIT). As a permissive license, it puts only very limited restriction on reuse and has therefore an excellent license compatibility. For detailed description of the contents of license please refer to the file [License](https://github.com/chrico7/data515_project/blob/master/LICENSE).

## Organization of the project

The project has the following structure:

```
data515_project/
  |- README.md
  |- data515_project/
     |-__init__.py
     |-kc_real_estate.py
     |-run.py
     |- data/
        |-kc/
        |-redfin/
     |- tests/
  |- Demo.ipynb
  |- docs/
     |- FunctionalSpec
     |- Designspec
     |- Projectplan
     |- TechnologyReview
     |- Final presentation
  |- examples/
  |- output/
  |- setup.py
  |- LICENSE
  |- requirements.txt
```
1: “More people are buying a home — the biggest financial decision of their lives — sight unseen”,  
    Seattle Times, 20 July 2018 [link](https://www.seattletimes.com/business/real-estate/more-people-are-buying-a-home-the-biggest-financial-decision-of-their-lives-sight-unseen/)  
    
2: See for example Congressional Research Service report: Introduction to U.S. Economy: Housing Market (October 2019)  
    https://fas.org/sgimes p/crs/misc/IF11327.pdf
