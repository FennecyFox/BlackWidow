# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class DuplicatePipeline(object):
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['source_url'] in self.urls_seen:
            raise DropItem('Duplicate item found: %s' % item)
        else:
            self.urls_seen.add(item['source_url'])

            return item


class NormalizationPipeline(object):
    def process_item(self, item, spider):
        title = item['title'][0]
        title = title.replace('Fancy - ', '')
        item['title'] = title

        image_urls = list(set(item['image_urls']))
        item['image_urls'] = image_urls

        return item


class DjangoModelStorePipeline(object):
    def process_item(self, item, spider):
        return item
