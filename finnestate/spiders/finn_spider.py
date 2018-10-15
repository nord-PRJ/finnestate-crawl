import scrapy


# scrapy runspider finn_spider.py


class FinnSpider(scrapy.Spider):
    name = 'finnhomes'
    start_urls = ['https://www.finn.no/realestate/homes/search.html?filters=']

    def parse(self, response):

        for entry in response.css('.mod .shadow .listing'):
            #print("HREF ",entry.xpath('//a[@data-search-resultitem=""]/@href').extract())

            yield {
                'id': entry.css('id ::text').extract_first(),
                'href': entry.xpath('//a[@data-search-resultitem=""]/@href').extract_first(),
                'location': entry.xpath('//a[@data-search-resultitem=""]/@href').extract_first(),
                'price': entry.css('a ::text').extract_first(),
                'square_meter': entry.css('a ::text').extract_first(),
                }

        #for next_page in response.css("//a[contains(.//text(), 'next')]"):
        #    yield response.follow(next_page, self.parse)

        #next_page = response.css('li.next a::attr(href)').extract_first()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse)