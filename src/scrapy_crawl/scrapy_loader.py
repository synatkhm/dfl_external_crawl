from scrapy.crawler import CrawlerProcess
from spiders.scrapy_crawl_new_aid import ScrapyCrawlNewAidSpider
import os, sys

if __name__ == "__main__":
    try:
        area_id=sys.argv[1]
        token=sys.argv[2]
        process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        })
        process.crawl(ScrapyCrawlNewAidSpider, area_id=area_id, token=token)
        process.start()
    except IndexError as e:
        print(f'Require city_id and area_id, Exception error')

       

