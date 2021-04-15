import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import time
class ScraperPubmed(scrapy.Spider):
    # scraper name
    name = "scraperpmc"
    
    # custom settings
    CUSTOM_SETTINGS = {'CONCURRENT_REQUESTS_PER_DOMAIN':1,
                      'DOWNLOAD_DELAY':1}
    secondary_keys=None
    import re
    # crawler's entry point
    def start_requests(self):
        import pandas as pd
        global secondary,li,LINKS
        Keys=pd.read_excel("input.xlsx")
        #seperating primary and secondary search word
        primary_keys = list(i for i in Keys["Search Keywords"])
        self.secondary_keys = list(i for i in Keys["2nd Generation Keywords"])
        #for j in range(0,len(primary_keys)):
        secondary= 'Uremic' # please enter the secondary key
        url='https://pubmed.ncbi.nlm.nih.gov/?term='
        url = url + 'desloratidine' +'&size=10' #  primary key key in middle
        #crawl through next search word
        yield scrapy.Request(
        url=url,callback=self.parse_pagination)
            
    # parse pagination callback function
    def parse_pagination(self, response):
        # loop over the range of pages
        for page in range(1,12):
            next_page= response.url + '&page=' +str(page)
            
            # crawl through the next_page
            yield response.follow(
                url = next_page,
                callback=self.parse_results
                )
            break
    # parse search result links
    def parse_results(self, response):
        
        # extract the links 
        links = response.css('div[class="docsum-content"]').css('a::attr(href)').getall()
        
        # loop over extracted links
        for Link in links:
            # crawl through sub links
            yield response.follow(
                url=Link,
                callback=self.parse_listing
                )
    # parse listing callback method
    def parse_listing(self,response):
        global secondary,li,LINKS
        try:
            abstract = response.css('div[class="abstract-content selected"]').css('p::text').getall()
            d=[]
            for i in range(len(abstract)):
                d.append(abstract[i].strip())
            Abstract=''
            for i in d:
                Abstract=Abstract+i
            word = secondary
            if self.re.search(r'\b{}\b'.format(self.re.escape(word)), Abstract):
                c = str(response).split('<200')
                c = c[-1].split('/>')
                c = c[0]
                LINKS=LINKS+[c]
            else:
                pass
            
        except:
            pass
if __name__=="__main__":
    begin = time.time()
    LINKS=[]
    secondary=''
    # seperating primary and secondary search word.
    process = CrawlerProcess()
    process.crawl(ScraperPubmed)
    process.start()
    
    print("\n\n Links:",LINKS)
    
    end = time.time() 
    print(f"\n\n Total runtime of the program is {end - begin}")