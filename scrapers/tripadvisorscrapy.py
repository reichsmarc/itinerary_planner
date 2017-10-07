# scrapes all activity info for a given country
import scrapy

class TripSpider(scrapy.Spider):
   name = 'tripadvisor_activities'

   custom_settings = {
                     "DOWNLOAD_DELAY": 0.1,
                     "CONCURRENT_REQUESTS_PER_DOMAIN": 15,
                     "HTTPCACHE_ENABLED": False
                      }

   start_urls = []
   for i in range(1,501):
      start_urls.append('https://www.tripadvisor.com/Attractions-g294073-Activities-t'+str(i)+'-Colombia.html')
      start_urls.append('https://www.tripadvisor.com/Attractions-g294073-Activities-c'+str(i)+'-Colombia.html')

   def parse(self, response): 
      activities = response.xpath('//div[@class="listing_title "]/a/@href').extract()
      for href in activities: # for each activity on activity pages (start_urls)
         yield response.follow(href, self.parse_activity,meta={'url':href}) # scrape all activity review pages

   def parse_activity(self, response):

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

      categories = response.xpath('//div[@class="detail"]/a/text()').extract()

      try:
         address = response.xpath('//span[@class="street-address"]/text()').extract()[0].strip()
      except IndexError:
         address = response.xpath('//span[@class="street-address"]/text()').extract()

      try:
         locality = response.xpath('//span[@class="locality"]/text()').extract()[0].strip()
      except IndexError:
         locality = response.xpath('//span[@class="locality"]/text()').extract()

      try:
         country = response.xpath('//span[@class="country-name"]/text()').extract()[0].strip()
      except IndexError:
         country = response.xpath('//span[@class="country-name"]/text()').extract()

      hoursopen = response.xpath('//div[@class="timeRanges ui_column is-8"]//text()').extract()
      days = response.xpath('//div[@class="dayRange ui_column is-4"]//text()').extract()

      try:
         recstay = response.xpath('//div[@class="detail_section duration"]//text()').extract()[0].strip()
      except IndexError:
         recstay = response.xpath('//div[@class="detail_section duration"]//text()').extract()

      try:
         description = response.xpath('//div[@class="modal-card-body"]/text()').extract()[0].strip()
      except IndexError:
         description = response.xpath('//div[@class="modal-card-body"]/text()').extract()

      url = response.request.meta['url']

      yield {
      'url': url,
      'title': title,
      'categories' : categories,
      'numreviews': numreviews,
      'overallrating': overallrating,
      'address': address,
      'locality': locality,
      'country': country,
      'hoursopen': hoursopen,
      'days': days,
      'recstay': recstay,
      'description': description
      }