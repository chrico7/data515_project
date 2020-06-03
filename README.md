# King County Real Estate Visualization Tool
----
Final project for DATA515 spring 2020

Buying a home is the largest single purchase that most people will make in their entire lives<sup>1</sup>. Additionally, the residential real estate market is one of the largest components of the American economy<sup>2</sup> and is closely regulated. Even so, good data on real estate trends and transactions is difficult to find and to access.

We address this problem locally with a tool that collects, cleans, joins and visualizes real estate administrative and listing data.

----

### Team members
Corey Christopherson<br/>
Richard Todd<br/>
Maggie Weatherly<br/>
Ruian Yang

### Software dependencies and license information

#### Programming language: 

- Python version 3.0 and above 

#### Packages:

- NumPy 1.11.1  
- pandas 1.0.4  
- matplotlib 1.5.3  
- geopanda 0.7.0 
- ipywidgets 7.5.1  

#### Installation:

$ conda install numpy pandas matplotlib<br/>
$ pip install geopanda<br/>
$ pip install ipywidgets

#### Licensing info:

The MIT License is a permissive free software license originating at the Massachusetts Institute of Technology (MIT). As a permissive license, it puts only very limited restriction on reuse and has therefore an excellent license compatibility. For detailed description of the contents of license please refer to the file [License](https://github.com/chrico7/data515_project/blob/master/LICENSE).

### Organization of the project

The project has the following structure:

```
data515_project/
  |- README.md
  |- code/
     |-get_county_data.py
     |-get_redfin_data.py
     |-join_county_redfin.py
     |-merge_kc_csvs.ipynb
     |-organize_county_data.py
     |-visualization_wip.ipynb
  |- data/
     |-kc/
     |-redfin/
  |- examples/
     |-interactive_notebook.ipynb
  |- docs/
     |- FunctionalSpec
     |- Designspec
     |- Projectplan
     |- TechnologyReview
     |- Final presentation
  |- setup.py
  |- LICENSE
  |- requirements.txt
```
1: “More people are buying a home — the biggest financial decision of their lives — sight unseen”,  
    Seattle Times, 20 July 2018 [link](https://www.seattletimes.com/business/real-estate/more-people-are-buying-a-home-the-biggest-financial-decision-of-their-lives-sight-unseen/)  
    
2: See for example Congressional Research Service report: Introduction to U.S. Economy: Housing Market (October 2019)  
    https://fas.org/sgimes p/crs/misc/IF11327.pdf