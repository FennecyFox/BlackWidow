# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html


class NormalizationPipeline(object):
    def process_item(self, item, spider):
        title = item['title'][0]
        title = title.replace('Fancy - ', '')
        item['title'] = title

        source_image_urls = list(set(item['source_image_urls']))
        item['source_image_urls'] = source_image_urls

        return item


class DjangoModelStorePipeline(object):
    def process_item(self, item, spider):
        return item
