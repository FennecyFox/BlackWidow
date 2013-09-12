# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from urlparse import urljoin
import re

from scrapy.exceptions import DropItem

from django.contrib.auth.models import User
from django.db.models import Q

from app_heels.models import Heels
from app_heels import tasks as heels_tasks
from app_reaper.models import Blacklist


class DefaultValuePipeline(object):

    def process_item(self, item, spider):
        item.setdefault('comment', '')
        item.setdefault('source_url', '')
        item.setdefault('image_urls', [])

        return item


class DuplicatePipeline(object):

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['source_url'] in self.urls_seen:
            raise DropItem('Duplicate item found: %s' % item['source_url'])
        else:
            self.urls_seen.add(item['source_url'])

            return item


class NormalizationPipeline(object):

    def process_item(self, item, spider):
        if len(item['image_urls']) == 0:
            raise DropItem('No image found: %s' % item['source_url'])

        try:
            comment = item['comment'][0]
        except IndexError:
            comment = ''
        item['comment'] = comment

        if spider.name == 'beautylegmm':
            new_image_urls = []
            for image_url in item['image_urls']:
                new_image_url = urljoin('http://www.beautylegmm.com/', image_url)
                new_image_urls.append(new_image_url)
            item['image_urls'] = new_image_urls

        elif spider.name == 'fancy':
            item['comment'] = comment.replace('Fancy - ', '')

        elif spider.name == 'garypeppergirl':
            new_image_urls = []
            for image_url in item['image_urls']:
                new_image_url = re.sub(r'\-\d+x\d+\.', '.', image_url)
                new_image_urls.append(new_image_url)

            item['image_urls'] = new_image_urls

        elif spider.name == 'ohmyvogue':
            item['comment'] = comment.replace('... Oh My Vogue !: ', '')

        elif spider.name == 'pinterest':
            if comment.startswith('. | '):
                comment = comment.replace('. | ')

            new_image_urls = []
            for image_url in item['image_urls']:
                if filter(image_url.endswith, ('.jpg', '.jpeg', '.gif', '.png')):
                    ori_image_url = image_url.replace('736x', 'originals')
                    new_image_urls.append(ori_image_url)

            item['image_urls'] = new_image_urls

        elif spider.name == 'wendyslookbook':
            comment = comment.replace(" : Wendy's Lookbook", '').replace('  :: ', ' :: ')
            item['comment'] = comment

            new_image_urls = []
            for image_url in item['image_urls']:
                new_image_url = re.sub(r'\-\d+x\d+\.', '.', image_url)
                new_image_urls.append(new_image_url)

            item['image_urls'] = new_image_urls

        item['image_urls'] = list(set(item['image_urls']))

        return item


class DjangoModelPipeline(object):

    def process_item(self, item, spider):
        ori_url = item['source_url']
        http_www_url = ori_url.replace('http://', 'http://www.')
        https_www_url = ori_url.replace('https://', 'https://www.')
        if Blacklist.objects.filter(Q(url=ori_url) | Q(url=http_www_url) | Q(url=https_www_url)).exists():
            raise DropItem('URL in blacklist: %s' % ori_url)

        user = User.objects.get(username='vinta')

        heels, created = Heels.objects.get_or_create(user=user, source_url=item['source_url'])
        if created:
            if item['comment']:
                heels.comment = item['comment'].strip()

            heels.source_image_urls = item['image_urls']

            if len(item['image_urls']) == 1:
                heels.source_image_url = item['image_urls'][0]

            heels.save()
        else:
            return item

        if created:
            if heels.source_image_url:
                # Celery task
                heels_tasks.save_heels_image.delay(heels.id, url=heels.source_image_url)

        return item
