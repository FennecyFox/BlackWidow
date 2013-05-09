from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from blackwidow.items import HeelsItem


class FancySpider(CrawlSpider):
    name = 'fancy'
    allowed_domains = ['www.thefancy.com', ]
    start_urls = [
        'http://www.thefancy.com/vinta',
    ]

    # http://doc.scrapy.org/en/latest/topics/spiders.html#crawling-rules
    # http://doc.scrapy.org/en/latest/topics/link-extractors.html#sgmllinkextractor
    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'vinta/fancyd/\d+', ),  # http://www.thefancy.com/vinta/fancyd/1360222057
                restrict_xpaths=('//div[@id="content"]//div[contains(@class, "pagination")]', ),
                unique=True,
            ),
            follow=True,
        ),
        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'things/\d+', ),  # http://www.thefancy.com/things/317225220580577663
                restrict_xpaths=('//div[@id="content"]/div[contains(@class, "stream")]', ),
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

        item['title'] = hxs.select('//title/text()').extract()

        center_image_urls = hxs.select('//div[contains(@id, "content")]/div[contains(@class, "figure-row")]/div//figure/span/span/img/@src').extract()
        sidebar_image_urls = hxs.select('//ul[contains(@class, "figure-list")]/li/a/@href').extract()
        item['image_urls'] = center_image_urls + sidebar_image_urls

        item['source_url'] = response.url

        return item
