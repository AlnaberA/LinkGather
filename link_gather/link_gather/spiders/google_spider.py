import scrapy
import validators


def write_to_crawled(data):
    with open("crawled.txt", "a+") as txt_file:
        # Move read cursor to the start of file.
        txt_file.seek(0)
        txt_file.write(data + '\n')


def is_crawled(data):
    with open('crawled.txt') as f:
        datafile = f.readlines()
    for line in datafile:
        if data in line:
            return True
    return False


def write_array_to_file(data):
    with open("output.txt", "w") as txt_file:
        for line in data:
            txt_file.write(line)


def convert_file_to_array():
    file = open("output.txt", "r")
    clean_string = file.read().strip('[').strip(']')
    return clean_string.split(',')


class GoogleSpider(scrapy.Spider):
    name = "googleSpider"

    start_urls = [
        'http://www.google.com'
    ]
    handle_httpstatus_list = [403, 404, 502]

    queue = []

    crawled = []

    def parse(self, response, **kwargs):
        links = response.css("a::attr(href)").getall()
        for link in links:
            if validators.url(link):
                if (link not in self.queue) and ('google.com' in link):
                    self.queue.append(link)

        next_page = self.queue[0]
        self.queue.pop(0)
        if not is_crawled(next_page):
            write_to_crawled(next_page)
        yield response.follow(next_page, callback=self.parse)
