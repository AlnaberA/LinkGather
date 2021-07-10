import scrapy


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

    def parse(self, response, **kwargs):
        write_array_to_file(str(response.css("a::attr(href)").getall()))
        test = convert_file_to_array()
        next_page = ''
