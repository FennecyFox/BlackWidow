# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from django.contrib.auth.models import User
from django.db import transaction

from app_heels.models import Heels
from app_heels import tasks as heels_tasks


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


class DjangoModelPipeline(object):
    def process_item(self, item, spider):
        user = User.objects.get(username='vinta')

        with transaction.commit_on_success():
            heels, created = Heels.objects.get_or_create(user=user, source_url=item['source_url'])
            if created:
                heels.comment = item['title']
                heels.source_image_urls = item['image_urls']

                if len(item['image_urls']) == 1:
                    heels.source_image_url = item['image_urls'][0]

                heels.save()

        if created:
            if heels.source_image_url:
                # Celery task
                heels_tasks.save_heels_image_from_url.delay(heels.id, heels.source_image_url)

        return item
