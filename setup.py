import setuptools

setuptools.setup(
    name="KingCountyRealEstate",
    version="1.0.0",
    author="Corey Christopherson, Richard Todd, Maggie Weatherly, Ruian Yang",
    author_email="coreyc2@uw.edu, ,mweath@uw.edu, ruiany@uw.edu",
    description="",
    long_description_content_type="text/markdown",
    url="https://github.com/chrico7/data515_project",
    packages=setuptools.find_packages(where='./data515_project', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'geopandas',
        'ipywidgets',
        'matplotlib',
        'numpy',
        'pandas',
        'plotly',
        'jupyter'
    ],
    python_requires='>=3.6',
)