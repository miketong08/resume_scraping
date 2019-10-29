# Resume Scraping via Craigslist

This repo contains Jupyter notebook tutorials in Python to perform webscraping, EDA, cleaning, and machine learning tasks such as classification and NLP.

__Classification and Machine learning__ - *Prince Mallari* (mallari\_prince@bah.com)  
__Webscraping__ - *Mike Tong* (tong\_michael@bah.com)

The data pulled is pulled over a couple of months at irregular intervals, which is compiled as `assets/data_large.csv`. Duplicates are dropped to keep the data as a single file while still meeting the github file size limitations, and contains about 60K unique samples with 8 features. 

Webscraping can be performed with `python -m scripts.scraping` . (Please make sure you have the correct chromedriver version for your particular Google Chrome in `assets/chromedriver`, see `notebooks/Webscraping.ipynb` for more details). A full run takes approximately 8 hours.

Please feel free to request pulls and add to the effort!
