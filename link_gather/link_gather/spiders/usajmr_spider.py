import scrapy


class UsajmrSpiderSpider(scrapy.Spider):
    name = 'usajmr_spider'
    allowed_domains = ['usajmr.com']
    start_urls = ['http://usajmr.com/']

    def parse(self, response):
        pass
