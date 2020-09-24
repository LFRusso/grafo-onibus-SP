# 
#   Scraping the cities bus connections
#
import scrapy

class MainSpider(scrapy.Spider):
    name = 'main-spider'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    base_url = 'https://www.temonibus.com/passagem-onibus/'
    start_urls = ['https://www.temonibus.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers)
        return

    def parse(self, response):
        
        # Getting all possible cities combinations 
        paths = []
        with open("data/combinacoes_sp.dat", "r") as file:
            line = file.readline()
            while(line):
                line = line[:-1]
                paths.append(line)
                line = file.readline()

        # Building the urls for each possible combination
        urls = ["{}{}".format(self.base_url, path) for path in paths]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_paths, headers=self.headers)
        
        return

    # Checks if the cities have connection by looking for a timetable for the bus
    def parse_paths(self, response):
        timetable = response.xpath("//div[@class='collection no-border']")
        if(len(timetable) != 0):
            print("Path found: {}".format(response.url))
            with open("data/caminhos.dat", 'a+') as file:
                file.write("{}\n".format(response.url))
        return