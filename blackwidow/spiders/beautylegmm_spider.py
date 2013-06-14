from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from blackwidow.items import HeelsItem


class FancySpider(CrawlSpider):
    name = 'beautylegmm'
    allowed_domains = ['www.beautylegmm.com', ]
    start_urls = [
        'http://www.beautylegmm.com/',
    ]

    # http://doc.scrapy.org/en/latest/topics/spiders.html#crawling-rules
    # http://doc.scrapy.org/en/latest/topics/link-extractors.html#sgmllinkextractor
    rules = (
        # # find next page
        # Rule(
        #     SgmlLinkExtractor(
        #         allow=(r'index\-\d+\.html', ),  # http://www.beautylegmm.com/index-2.html
        #         restrict_xpaths=('//*[@id="pages"]', ),
        #         unique=True,
        #     ),
        #     follow=True,
        # ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\w+/beautyleg\-\d+\.html', ),  # http://www.beautylegmm.com/Susan/beautyleg-816.html
                restrict_xpaths=('//*[@id="content"]', ),
                unique=True,
            ),
            callback='parse_product_detail',
        ),
    )

    def parse_product_detail(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the
        start_urls attribute of the Spider, and assigns them the parse method
        of the spider as their callback function.
        """

        hxs = HtmlXPathSelector(response)

        item = HeelsItem()

        item['comment'] = hxs.select('//*[@id="contents"]/div[5]/p[1]/text()').extract()
        item['image_urls'] = hxs.select('//*[@id="contents"]/div[5]//img/@src').extract()
        item['source_url'] = response.url

        return item
