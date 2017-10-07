# scrapes all hostel info for a given country
import scrapy
import pandas as pd

class TripSpider(scrapy.Spider):
   name = 'tripadvisor_hostels'

   custom_settings = {
                     "DOWNLOAD_DELAY": 0.1,
                     "CONCURRENT_REQUESTS_PER_DOMAIN": 15,
                     "HTTPCACHE_ENABLED": False
                      }

   start_urls = ['https://www.tripadvisor.com/']

   def parse(self, response): 

      urls = pd.read_pickle('/Users/marc/hreflist.pkl')
      hrefs = []
      for url in urls:
         hrefs.append(url.replace('https://www.tripadvisor.com/',''))

      for href in hrefs:
         yield response.follow(href, self.parse_hostel,meta={'url':href}) # scrape all hostel review pages

   def parse_hostel(self, response):

      try:
         title = response.xpath('//h1[@id="HEADING"]/text()').extract()[0].strip()
      except IndexError: 
         title = response.xpath('//h1[@id="HEADING"]/text()').extract()

      try:
         numreviews = response.xpath('//a/span[@property="v:count"]/text()').extract()[0].strip()
      except IndexError:
         numreviews = response.xpath('//a/span[@property="v:count"]/text()').extract()

      try:
         overallrating = response.xpath('//span[@class="overallRating"]/text()').extract()[0].strip()
      except IndexError:
         overallrating = response.xpath('//span[@class="overallRating"]/text()').extract()

      try:
         address = response.xpath('//span[@class="street-address"]/text()').extract()[0].strip()
      except IndexError:
         address = response.xpath('//span[@class="street-address"]/text()').extract()

      try:
         ext_address = response.xpath('//span[@class="extended-address"]/text()').extract()[0].strip()
      except IndexError:
         ext_address = response.xpath('//span[@class="extended-address"]/text()').extract()

      try:
         locality = response.xpath('//span[@class="locality"]/text()').extract()[0].strip()
      except IndexError:
         locality = response.xpath('//span[@class="locality"]/text()').extract()

      try:
         country = response.xpath('//span[@class="country-name"]/text()').extract()[0].strip()
      except IndexError:
         country = response.xpath('//span[@class="country-name"]/text()').extract()


      try: 
         avgprice = response.xpath('//ul[@class="list price_range"]/li/text()').extract()[1].strip()
      except IndexError:
         avgprice = response.xpath('//ul[@class="list price_range"]/li/text()').extract()

      url = response.request.meta['url']

      yield {
      'url': url,
      'title': title,
      'numreviews': numreviews,
      'overallrating': overallrating,
      'address': address,
      'ext_address' : ext_address,
      'locality': locality,
      'country': country,
      'avgprice': avgprice
      }