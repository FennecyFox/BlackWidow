import math
import urlparse

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from blackwidow.items import HeelsItem


PINS_PER_PAGE = 50.0


class PinterestSpider(BaseSpider):
    """
    For old UI
    """

    name = 'pinterest'
    allowed_domains = ['pinterest.com', ]
    start_urls = [
        'http://pinterest.com/vintalines/pins/?filter=likes&page=1',
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        total_liked_pins = int(hxs.select('//*[@id="ContextBar"]/div/ul[1]/li[3]/a/strong/text()').extract()[0])
        pages = int(math.ceil(total_liked_pins / PINS_PER_PAGE))
        for page in xrange(1, pages + 1):
            next_url = 'http://pinterest.com/vintalines/pins/?filter=likes&page=%d' % (page)
            yield Request(next_url, callback=self.parse_pin_list)

    def parse_pin_list(self, response):
        hxs = HtmlXPathSelector(response)

        pin_urls = hxs.select('//*[@id="ColumnContainer"]/div[contains(@class, "pin")]/div[contains(@class, "PinHolder")]/a/@href').extract()
        for pin_url in pin_urls:
            pin_url = urlparse.urljoin('http://pinterest.com/', pin_url)
            yield Request(pin_url, callback=self.parse_pin_detail)

    def parse_pin_detail(self, response):
        if getattr(self, 'close_by_pipeline', None):
            # only can call in spider, can not call in pipeline
            raise CloseSpider('Stop')

        item = HeelsItem()

        hxs = HtmlXPathSelector(response)

        item['image_urls'] = hxs.select('//*[@id="PinImageHolder"]/a/@href').extract()
        if not filter(item['image_urls'][0].endswith, ('.jpg', '.jpeg', '.gif', '.png')):
            item['image_urls'] = hxs.select('//*[@id="pinCloseupImage"]/@src').extract()

        item['source_url'] = response.url

        return item


class PinterestNewSpider(CrawlSpider):
    """
    For new UI, you need to login
    """

    name = 'pinterest_new'
    allowed_domains = ['pinterest.com', ]
    login_page = 'https://pinterest.com/login/'
    start_urls = [
        'http://pinterest.com/vintalines/likes/',
    ]

    # http://doc.scrapy.org/en/latest/topics/spiders.html#crawling-rules
    # http://doc.scrapy.org/en/latest/topics/link-extractors.html#sgmllinkextractor
    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'vintalines/likes', ),
                # restrict_xpaths=('//div[@id="content"]//div[contains(@class, "pagination")]', ),
                unique=True,
            ),
            follow=True,
        ),
        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'pin/\d+', ),  # http://pinterest.com/pin/7810999325432246/
                # restrict_xpaths=('//div[contains(@class, "UserProfileContent")]/div[contains(@class, "padItems")]', ),
                # unique=True,
            ),
            callback='parse_pin_detail',
        ),
    )

    def start_requests(self):
        """
        This function is called before crawling starts.
        """

        return [Request(url=self.login_page, callback=self.login), ]

    def login(self, response):
        hxs = HtmlXPathSelector(response)

        PINTEREST_USERNAME = self.settings['PINTEREST_USERNAME']
        PINTEREST_PASSWORD = self.settings['PINTEREST_PASSWORD']

        login_info = {
            'email': PINTEREST_USERNAME,
            'password': PINTEREST_PASSWORD,
            'csrfmiddlewaretoken': hxs.select('//*[@id="AuthForm"]/ul/div[1]/input/@value').extract()[0],
            'ch': hxs.select('//*[@id="AuthForm"]/ul/div[2]/input/@value').extract()[0],
        }

        return FormRequest.from_response(response,
                                         formdata=login_info,
                                         callback=self.check_login_response,
                                         dont_filter=True)

    def check_login_response(self, response):
        """
        Check the response returned by a login request to see if we are
        successfully logged in.
        """

        # Something went wrong, we couldn't log in, so nothing happens.
        if not 'Vinta' in response.body:
            self.log('Login fail')
            raise

        self.log("Successfully logged in. Let's start crawling!")

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse_pin_detail(self, response):
        item = HeelsItem()

        return item
