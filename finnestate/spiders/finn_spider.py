import scrapy


# scrapy runspider finn_spider.py
class FinnSpider(scrapy.Spider):
    name = 'finnhomes_top_layer'
    start_urls = ['https://www.finn.no/realestate/homes/search.html?filters=']
    base_url = "https://www.finn.no"

    def parse(self, response):
        main_section = response.css('.main-section')
        result_hit_count = response.xpath('//div[@role="main"]/@data-result-hit-count').extract_first()
        print("result hit count: "+result_hit_count)
        for i , entry in enumerate(main_section.css('.result-item')):
            if entry.css('span.mrs ::text').extract_first():
                continue # ignore weekly ad med ukens bolig
            yield {
                'id': entry.xpath('//a/@data-finnkode').extract()[i],
                'href': self.base_url + entry.xpath('//a[@data-search-resultitem=""]/@href').extract()[i],
                'img_href': entry.css('img.centered-image').xpath('@src').extract_first(),
                'real_estate_firm': entry.css('li.truncate ::text').extract_first(),
                'location': entry.css('div.valign-middle ::text').extract_first(),
                'square_meter': entry.css('span.prm ::text').extract_first(), #square meter is the first span
                'price': entry.css('span.prm:last-child ::text').extract()[0], #price is secon span
                'owner': entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[0],
                'building_type': entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[1],
                'rooms': entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[2],
                'ad_title': entry.css('h3.result-item-heading ::text').extract_first(),
                }

        #for next_page in response.css("//a[contains(.//text(), 'next')]"):
        #    yield response.follow(next_page, self.parse)

        #next_page = response.css('li.next a::attr(href)').extract_first()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse)
