import scrapy
import validators


def write_to_crawled(data):
    with open("crawled.txt", "a+") as txt_file:
        # Move read cursor to the start of file.
        txt_file.seek(0)
        txt_file.write(data + '\n')


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
        'http://www.usajmr.com'
    ]

    queue = []

    crawled = []

    def parse(self, response, **kwargs):
        next_page = ''
        links = response.css("a::attr(href)").getall()
        for link in links:
            if validators.url(link):
                self.queue.append(link)

        # Alaa - There is a bug here, L#44 element is being removed before the page is crawled.
        for element in self.queue:
            self.queue.remove(element)
            if element not in self.crawled:
                self.crawled.append(element)
                # write_to_crawled(element)
            next_page = element
        yield response.follow(next_page, callback=self.parse)
