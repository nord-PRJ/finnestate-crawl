import scrapy


# scrapy runspider finn_spider.py
class FinnSpider(scrapy.Spider):
    name = 'finnhomes_top_layer'
    start_urls = ['https://www.finn.no/realestate/homes/search.html?filters=']
    base_url = "https://www.finn.no"
    pages_parsed = 1
    entries = 0

    def parse(self, response):
        main_section = response.css('.main-section')
        result_hit_count = response.xpath('//div[@role="main"]/@data-result-hit-count').extract_first()

        print("result hit count: "+result_hit_count)
        print("Page: "+ str(self.pages_parsed))

        for i , entry in enumerate(main_section.css('.result-item')):
            self.entries += 1
            print("Entry Number: "+ str(self.entries))

            # ignore weekly ad med ukens bolig
            if entry.css('span.mrs ::text').extract_first():
                print("skipped entry due to ad")
                continue

            # Common Debt and Common Entry - Same line extract
            common_debt = None
            common_expenses = None
            if entry.css('li.hide-lt768 ::text').extract_first():
                common_debt=entry.css('li.hide-lt768 ::text').extract_first().split(u' \u2022 ')[0]
                if not len(entry.css('li.hide-lt768 ::text').extract_first().split(u' \u2022 ')) is 1: # check if list is larger than one, second element should be common_expenses
                    common_expenses = entry.css('li.hide-lt768 ::text').extract_first().split(u' \u2022 ')[1]

            #Owner Building Type and Rooms - Same extract
            owner = None
            building_type = None
            rooms = None
            if entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first():
                entry_len = len(entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first())
                print(entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 '))
                if entry_len is 1:
                    print("in here")
                    owner = entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[0];
                elif entry_len is 2:
                    owner = entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[0];
                    building_type = entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[1];
                elif entry_len is 3:
                    owner = entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[0];
                    building_type = entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[1];
                    rooms = entry.css('li[data-automation-id="bottomRow2"] ::text').extract_first().split(u' \u2022 ')[2];

            #Price check as sometimes price isnt labeled
            price = None;
            if entry.css('span.prm:last-child ::text').extract():
                price = entry.css('span.prm:last-child ::text').extract()[0];

            yield {
                'id': entry.xpath('//a/@data-finnkode').extract()[i],
                'href': self.base_url + entry.xpath('//a[@data-search-resultitem=""]/@href').extract()[i],
                'img_href': entry.css('img.centered-image').xpath('@src').extract_first(),
                'real_estate_firm': entry.css('li.truncate ::text').extract_first(),
                'location': entry.css('div.valign-middle ::text').extract_first(),
                'square_meter': entry.css('span.prm ::text').extract_first(), #square meter is the first span
                'price': price, #price is secon span
                'owner': owner,
                'building_type': building_type,
                'rooms': rooms,
                'ad_title': entry.css('h3.result-item-heading ::text').extract_first(),
                'common_debt': common_debt,
                'common_expenses': common_expenses,
                }
            print("-"*30);
        
        for next_page in response.css("a.pam").xpath('@href'):
            yield response.follow(next_page, self.parse)

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            self.pages_parsed += 1
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
