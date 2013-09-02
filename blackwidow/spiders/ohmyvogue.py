from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from blackwidow.items import HeelsItem


class WendysLookbookSpider(CrawlSpider):
    name = 'ohmyvogue'
    allowed_domains = ['www.ohmyvogue.com', ]
    start_urls = [
        'http://www.ohmyvogue.com/',
    ]

    # http://doc.scrapy.org/en/latest/topics/spiders.html#crawling-rules
    # http://doc.scrapy.org/en/latest/topics/link-extractors.html#sgmllinkextractor
    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'search\?updated-max=', ),  # http://www.ohmyvogue.com/search?updated-max=2013-08-27T11:07:00%2B02:00&max-results=3
                restrict_xpaths=('//*[@id="blog-pager-older-link"]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+\/\d+\/[\w-]+\.html', ),  # http://www.ohmyvogue.com/2013/08/nude-white.html
                restrict_xpaths=('//*[@id="Blog1"]/div[contains(@class, "blog-posts")]', ),
                unique=True,
            ),
            callback='parse_post_detail',
        ),
    )

    def parse_post_detail(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the
        start_urls attribute of the Spider, and assigns them the parse method
        of the spider as their callback function.
        """

        hxs = HtmlXPathSelector(response)

        item = HeelsItem()

        item['comment'] = hxs.select('//title/text()').extract()
        item['image_urls'] = hxs.select('//*[@id="Blog1"]//div[contains(@class, "post-body")]//img/@src').extract()
        item['source_url'] = response.url

        return item
