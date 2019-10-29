# python3.6                                                         
"""./ancillary.py
Contains helper functions for the notebooks

CREATED AUG-2019: Mike Tong - tong_michael@bah.com
"""
import numpy as np


def parse_webpage_table(table):                                    
    """Accepts a selenium WebElement table of zip codes information from
    http://localistica.com/usa/zipcodes/most-populated-zipcodes/ and
    returns a list of only zip codes.
    :param table: selenium.webdriver.remote.webelement.WebElement class

    :return: list of zip codes as integers
    """                                                            
    parsed_table = table.text.split('\n')                          

    # first element is header                                      
    zipcodes = [i.split()[0] for i in parsed_table[1:]]            
    cities = []                                                    
    for row in parsed_table[1:]:                                   
        split_row = row.split()

        # abbreviation is uppercase only                           
        abbrev = [i for i, v in enumerate(split_row) if v.isupper()]
        cities.append(''.join(split_row[1:abbrev[0]]))             

    return list(zip(cities, zipcodes))


def update_search_page(url, page):
    """docstring tbd"""
    
    url_num = page * 120

    # if search number does not exist
    if url.find('s=') == -1:
        start_loc = url.find('?') + 1
        return url[:start_loc] + "s={}&".format(url_num) + url[start_loc:]

    else:
        start_loc = url.find('s=')
        end_loc = url[start_loc:].find('&') + start_loc
        return url[:start_loc] + 's={}'.format(url_num) + url[end_loc:]


def get_num_images(driver, url):
    """Calculates the number of images on a CL posting
    :param driver: The current webdriver class
    :param url: The url to count images from
    
    :return: The number of images on a CL posting as an int
    """
    driver.get(url)
    try:
        image_def = driver.find_element_by_xpath('/html/body/section/section/section/figure').get_attribute('class')
        if image_def == 'iw oneimage':
            return 1
        else:
            return len(driver.find_element_by_xpath('//*[@id="thumbs"]').find_elements_by_tag_name('a'))

    except:
        return 0


def get_education(driver, url):
    """Pulls education data from the webpage
    :param driver: The current webdriver class
    :param url: The url to pull education data from
    
    :return: The craigslist education level
    """
    driver.get(url)
    try:
        paths = driver.find_elements_by_xpath(
            '/html/body/section/section/section/div[1]/p/span')
        
        # sometimes the last item is a license
        education = [i.text for i in paths if i.text.find('education') != -1]
        if len(education) == 0:
            return education[0].split(':')[-1].strip()
        else:
            return np.nan
    except:
        return np.nan
    
