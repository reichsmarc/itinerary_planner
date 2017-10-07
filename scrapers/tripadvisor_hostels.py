
# coding: utf-8

# In[11]:


import os
import pandas as pd
import numpy as np
import random
from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time


# In[12]:


## Get Hostel URLs
# driver = webdriver.Firefox()
# driver.get('https://www.tripadvisor.com/Hotels-g294073-c3-Colombia-Hotels.html')

# nextlink = driver.find_element_by_xpath('//div[@class="unified pagination standard_pagination"]/span[@class="nav next taLnk ui_button primary"]')
# nextlink.click()

# hrefs = []
# while True:
#     try:
#         WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'div.listing_title')))
#         new_hrefs = [x.get_attribute('href') for x in driver.find_elements_by_xpath('//div[@class="listing_title"]//a')]
        
#     except:
#         print("Stale element. Retrying...")
#         WebDriverWait(driver,120).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'div.listing_title')))
#         new_hrefs = [x.get_attribute('href') for x in driver.find_elements_by_xpath('//div[@class="listing_title"]//a')]

#     hrefs.append(new_hrefs)
    
#     try:
#         nextlink = driver.find_element_by_xpath('//div[@class="unified pagination standard_pagination"]/span[@class="nav next taLnk ui_button primary"]')
#         nextlink.click()
#     except:
#         break
# driver.close()


# In[5]:


# # Flatten list
# hreflist = [item for sublist in hrefs for item in sublist]
# pd.to_pickle(hreflist,'hreflist.pkl')


# In[6]:


hreflist = pd.read_pickle('hreflist.pkl')


# In[32]:


t0 = time.time()

display = Display(visible=0, size=(1024, 768))
display.start()

print('Scraping',len(hreflist),'URLs...')
hostelnum = 0
    
for i,href in enumerate(hreflist):

    print("scraping:",href)
    hostelnum += 1
    pagenum = 0

    get_ipython().magic('time driver = webdriver.Firefox()')
    get_ipython().magic('time driver.get(href)')

    while pagenum<100:
        reviewpages = {}

        t1 = time.time()

        pagenum += 1

        # wait for page to load and scrape reviews, titles, dates and usernames
        #WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'div.prw_rup.prw_reviews_text_summary_hsx div.entry p.partial_entry')))

        # find and click "more" button to expand review text 
        try:
            driver.find_element_by_xpath('//span[@class="taLnk ulBlueLinks"]').click()
        except:
            print("No 'more' button found.")
            pass

        # save review data
#         WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'div.prw_rup.prw_reviews_text_summary_hsx div.entry p.partial_entry')))
        try:
            reviews = [[x.text] for x in driver.find_elements_by_css_selector('div.prw_rup.prw_reviews_text_summary_hsx div.entry p.partial_entry')]
            reviewtitles = [[x.text] for x in driver.find_elements_by_xpath('//span[@class="noQuotes"]')]
            reviewdates = [[x.get_property('title')] for x in driver.find_elements_by_xpath('//span[@class="ratingDate relativeDate"]')]
            usernames = [[x.text] for x in driver.find_elements_by_xpath('//span[@class="expand_inline scrname"]')]
            ratings = [[x.get_attribute("class")] for x in driver.find_elements_by_xpath('//div[@class="rating reviewItemInline"]/span[1]')]
            
        except:
            print("Stale element. Retrying...")
            WebDriverWait(driver,30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'div.prw_rup.prw_reviews_text_summary_hsx div.entry p.partial_entry')))
            reviews = [[x.text] for x in driver.find_elements_by_css_selector('div.prw_rup.prw_reviews_text_summary_hsx div.entry p.partial_entry')]
            reviewtitles = [[x.text] for x in driver.find_elements_by_xpath('//span[@class="noQuotes"]')]
            reviewdates = [[x.get_property('title')] for x in driver.find_elements_by_xpath('//span[@class="ratingDate relativeDate"]')]
            usernames = [[x.text] for x in driver.find_elements_by_xpath('//span[@class="expand_inline scrname"]')]
            ratings = [[x.get_attribute("class")] for x in driver.find_elements_by_xpath('//div[@class="rating reviewItemInline"]/span[1]')]

        # store page in dictionary
        reviewpages[href+'{}'+str(pagenum)] = [reviews,reviewtitles,reviewdates,usernames,ratings]

        print("Scraped Hostel #",hostelnum,"; Review Page #",pagenum)

        t2 = time.time()
        print(np.round(t2-t1,3),"sec")

        # find and click 'next' button
        try:
            nextlink = driver.find_element_by_xpath('//span[@class="nav next taLnk "]')
            nextlink.click()
        except:
            break

        with open('hostel_reviews_json/reviews{0}.json'.format(str(i)+'_'+str(pagenum)), 'w') as fp:
            json.dump(reviewpages, fp)
        
    driver.close()

tf = time.time()
print("Total run time:",np.round(tf-t0,3),"sec elapsed")

