import os
import scrapy
import validators

CRAWLED_FILE = "crawled.txt"
OUTPUT_FILE = "output.txt"


def write_to_crawled(data):
    with open(CRAWLED_FILE, "a") as txt_file:
        txt_file.write(data + '\n')


def is_crawled(data):
    if not os.path.exists(CRAWLED_FILE):
        open(CRAWLED_FILE, 'a').close()
        return False
    with open(CRAWLED_FILE) as f:
        return data in f.read()


def write_array_to_file(data):
    with open(OUTPUT_FILE, "w") as txt_file:
        for line in data:
            txt_file.write(line)


def convert_file_to_array():
    with open(OUTPUT_FILE, "r") as file:
        clean_string = file.read().strip('[').strip(']')
        return clean_string.split(',')


class GoogleSpider(scrapy.Spider):
    name = "googleSpider"

    start_urls = [
        'http://www.google.com'
    ]
    handle_httpstatus_list = [403, 404, 502]

    queue = set()
    crawled = set()

    def parse(self, response, **kwargs):
        links = response.css("a::attr(href)").getall()
        for link in links:
            if validators.url(link):
                if link not in self.queue and 'google.com' in link:
                    self.queue.add(link)

        if self.queue:
            next_page = self.queue.pop()
            if not is_crawled(next_page):
                write_to_crawled(next_page)
            yield response.follow(next_page, callback=self.parse)
