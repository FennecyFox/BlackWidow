import math
import urlparse

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from blackwidow.items import HeelsItem


# class PinterestSpider(BaseSpider):
#     """
#     For old UI
#     """

#     name = 'pinterest'
#     allowed_domains = ['pinterest.com', ]
#     start_urls = [
#         'http://pinterest.com/vintalines/pins/?filter=likes&page=1',
#     ]

#     def parse(self, response):
#         hxs = HtmlXPathSelector(response)

#         total_liked_pins = int(hxs.select('//*[@id="ContextBar"]/div/ul[1]/li[3]/a/strong/text()').extract()[0])
#         pages = int(math.ceil(total_liked_pins / PINS_PER_PAGE))
#         for page in xrange(1, pages + 1):
#             next_url = 'http://pinterest.com/vintalines/pins/?filter=likes&page=%d' % (page)
#             yield Request(next_url, callback=self.parse_pin_list)

#     def parse_pin_list(self, response):
#         hxs = HtmlXPathSelector(response)

#         pin_urls = hxs.select('//*[@id="ColumnContainer"]/div[contains(@class, "pin")]/div[contains(@class, "PinHolder")]/a/@href').extract()
#         for pin_url in pin_urls:
#             pin_url = urlparse.urljoin('http://pinterest.com/', pin_url)
#             yield Request(pin_url, callback=self.parse_pin_detail)

#     def parse_pin_detail(self, response):
#         if getattr(self, 'close_by_pipeline', None):
#             # only can call in spider, can not call in pipeline
#             raise CloseSpider('Stop')

#         item = HeelsItem()

#         hxs = HtmlXPathSelector(response)

#         item['image_urls'] = hxs.select('//*[@id="PinImageHolder"]/a/@href').extract()
#         if item['image_urls']:
#             if not filter(item['image_urls'][0].endswith, ('.jpg', '.jpeg', '.gif', '.png')):
#                 item['image_urls'] = hxs.select('//*[@id="pinCloseupImage"]/@src').extract()
#         else:
#             item['image_urls'] = hxs.select('//*[@id="pinCloseupImage"]/@src').extract()

#         item['source_url'] = response.url

#         return item


class PinterestSpider(CrawlSpider):
    name = 'pinterest'
    allowed_domains = ['pinterest.com', ]
    start_urls = [
        'http://pinterest.com/vintalines/likes/',
    ]

    # http://doc.scrapy.org/en/latest/topics/spiders.html#crawling-rules
    # http://doc.scrapy.org/en/latest/topics/link-extractors.html#sgmllinkextractor
    rules = (
        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'pin/\d+/$', ),  # http://pinterest.com/pin/128141551870912604/
                unique=True,
            ),
            callback='parse_pin_detail',
        ),
    )

    def parse_pin_detail(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the
        start_urls attribute of the Spider, and assigns them the parse method
        of the spider as their callback function.
        """

        hxs = HtmlXPathSelector(response)

        item = HeelsItem()

        item['comment'] = hxs.select('//title/text()').extract()

        urls_1 = hxs.select('//div[contains(@class, "pinWrapper")]//div[contains(@class, "pinImageSourceWrapper")]//img/@src').extract()
        urls_2 = hxs.select('//div[contains(@class, "pinWrapper")]//div[contains(@class, "pinImageSourceWrapper")]//a/@href').extract()
        item['image_urls'] = urls_1 + urls_2

        item['source_url'] = response.url

        return item
