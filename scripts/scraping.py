# python3.6
"""./scraping.py
Performs webscraping of resumes on craigslist

CREATED OCT-2019: Mike Tong - tong_michael@bah.com
"""

from collections import defaultdict
import datetime
import pickle

from selenium import webdriver
import pandas as pd

from .ancillary import get_num_images, get_education


class CraigslistScrapper():
    def __init__(self, driver, locations):
        self.driver = driver
        self.locations = locations
        
    # Function 1 to go to a particular webpage
    def cl_resume_area(self, city, zipcode, distance=9999):
        return self.driver.get(
            "https://{}.craigslist.org/d/resumes/search/rrr?postal={}&search_distance={}".format(city, zipcode, distance))
    
    # Function 2 to get all the associate URLs for the location.
    def extract_urls(self):
        self.urls = []
        
        # try statement to check if page exists
        try: 
            n_pages = int(self.driver.find_element_by_xpath(
                '//*[@id="searchform"]/div[3]/div[3]/span[2]/span[3]/span[2]').text) // 120 + 1

            for page in range(n_pages):
                self.driver.get(update_search_page(self.driver.current_url, page))
                cl_results = self.driver.find_element_by_xpath('//*[@id="sortable-results"]/ul')
                cl_results_items = cl_results.find_elements_by_tag_name("li")
                for item in cl_results_items:
                    self.urls.append(item.find_element_by_tag_name('a').get_attribute('href'))
        
        except:
            return self.urls
        
    # Function for 3 to get content
    def extract_resume_content(self, url):
        self.driver.get(url)
        return self.driver.find_element_by_xpath('//*[@id="postingbody"]').text
        
    # addtional function to determine if location is in a diff area i.e. NJ w/ NYC search
    def extract_nearby_location(self):
        return self.driver.find_element_by_xpath(
            '//*[@id="sortable-results"]/ul/li[1]/p/span[2]/span[1]').get_attribute('title')
    
    # Looping over all locations and saving as a dataframe
    def execute_scrape(self):
        self.raw_data = defaultdict(list)
        
        for city, zipcode in self.locations:
            self.cl_resume_area(city, zipcode)
            self.extract_urls()
            for url in self.urls:
                try:
                    contents = self.extract_resume_content(url)

                    date = get_posting_date(self.driver)
                    edu = get_education(self.driver)
                    n_photos = get_num_images(self.driver)
                    avail = get_availability(self.driver)
                
                except:
                    continue
                    
                try:
                    city = self.extract_nearby_location()
                except:
                    pass
                
                self.raw_data['city'].append(city)
                self.raw_data['searched_zipcode'].append(zipcode)
                self.raw_data['url'].append(url)
                self.raw_data['content'].append(contents)
                self.raw_data['posting_date'].append(date)
                self.raw_data['education'].append(edu)
                self.raw_data['n_photos'].append(n_photos)
                self.raw_data['availability'].append(avail)
                
                
def main(driver_path, webpage_table_path, save_path):
    driver = webdriver.Chrome(driver_path)
    
    with open(webpage_table_path, "rb") as f:
        webpage_table_info = pickle.load(f)
        
    scraper = CraigslistScrapper(driver, webpage_table_info)
    scraper.execute_scrape()
    
    df = pd.DataFrame(scraper.raw_data)
    df.to_csv(save_path)
    
    return df
    

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--driver_path',
                        help='Path to chromedriver', 
                        default='./assets/chromedriver'
                       )
    parser.add_argument('-s', '--save_path',
                        help='Path to save data', 
                        default="./assets/data_large_{}.csv".format(
                            str(datetime.datetime.now().date().strftime("%d%m%y")))
                       )
    parser.add_argument('-w', '--webpage_path',
                        help='Path to the webpage table pkl', 
                        default="./assets/webpage_table_info.pkl"
                       )
    args = parser.parse_args()
    
    main(args.driver_path, args.webpage_path, args.save_path)