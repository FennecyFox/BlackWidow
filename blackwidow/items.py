# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.contrib_exp.djangoitem import DjangoItem
from scrapy.item import Item, Field


class HeelsItem(Item):
    title = Field()
    source_url = Field()
    image_urls = Field()
    images = Field()
