from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from blackwidow.items import HeelsItem


class TVCClubSpider(CrawlSpider):

    name = 'tvcclub'
    allowed_domains = ['tvcclub.com', ]
    start_urls = [
        'http://tvcclub.com/index.php?mid=Korean_Grils',
        # 'http://tvcclub.com/index.php?mid=Japan_Grils',
        'http://tvcclub.com/index.php?mid=Asia_Grils',
    ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'index.php\?mid=\w+_Grils&page=\d+', ),  # http://tvcclub.com/index.php?mid=Korean_Grils&page=2
                restrict_xpaths=('//*[@id="bd"]/form', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'index.php\?mid=\w+_Grils&document_srl=\d+', ),  # http://tvcclub.com/index.php?mid=Korean_Grils&document_srl=44884
                restrict_xpaths=('//*[@id="tmb_lst"]', ),
                unique=True,
            ),
            callback='parse_post_detail',
        ),
    )

    def parse_post_detail(self, response):
        hxs = HtmlXPathSelector(response)

        item = HeelsItem()
        item['comment'] = hxs.select('//title/text()').extract()
        item['image_urls'] = hxs.select('//*[@id="bd"]//div[contains(@class, "rd_body")]//img/@src').extract()
        item['source_url'] = response.url

        return item
