# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class HeelsItem(Item):
    title = Field()
    source_image_urls = Field()
    source_url = Field()
    crawled = Field()
