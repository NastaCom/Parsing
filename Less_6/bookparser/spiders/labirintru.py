import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5/?stype=0']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        price_old = response.xpath("//div[@class='buying-priceold-val']/span/text()").get()
        price_new = response.xpath("//div[@class='buying-pricenew-val']/span/text()").get()
        authors = response.xpath("//div[@class='authors']/a/text()").getall()
        rate = response.xpath("//div[@id='rate']/text()").get()
        link = response.url
        item = BookparserItem(name=name, price_old=price_old, price_new=price_new, authors=authors, rate=rate, link=link)
        yield item

