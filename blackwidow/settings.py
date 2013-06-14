# Scrapy settings for blackwidow project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os


BOT_NAME = 'BlackWidow'
WEBSITE = 'http://heelsfetishism.com'
USER_AGENT = '%s/1.0 (+%s)' % (BOT_NAME, WEBSITE)
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en',
}

SPIDER_MODULES = ['blackwidow.spiders']
NEWSPIDER_MODULE = 'blackwidow.spiders'

DEFAULT_ITEM_CLASS = 'blackwidow.items.HeelsItem'

# COOKIES_DEBUG = True

LOG_STDOUT = True

# http://doc.scrapy.org/en/latest/topics/feed-exports.html
# store result in file
FEED_FORMAT = 'json'
FEED_URI = 'result.json'

ITEM_PIPELINES = [
    'blackwidow.pipelines.DefaultValuePipeline',
    'blackwidow.pipelines.DuplicatePipeline',
    'blackwidow.pipelines.NormalizationPipeline',
    'blackwidow.pipelines.DjangoModelPipeline',
    # 'scrapy.contrib.pipeline.images.ImagesPipeline',
]

# http://doc.scrapy.org/en/latest/topics/images.html
# save images to disk
if 'scrapy.contrib.pipeline.images.ImagesPipeline' in ITEM_PIPELINES:
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    IMAGES_STORE = os.path.join(PROJECT_PATH, 'images')
    IMAGES_MIN_WIDTH = 400


# http://jonathanstreet.com/blog/django-scrapy/
def setup_django_env(django_settings_dir):
    import imp
    import sys

    from django.core.management import setup_environ

    django_project_path = os.path.abspath(os.path.join(django_settings_dir, '..'))
    sys.path.append(django_project_path)
    sys.path.append(django_settings_dir)

    f, filename, desc = imp.find_module('settings', [django_settings_dir, ])
    project = imp.load_module('settings', f, filename, desc)

    setup_environ(project)

# where Django settings.py placed
DJANGO_SETTINGS_DIR = '/all_projects/heelsfetishism/heelsfetishism'

try:
    from settings_prod import *
except ImportError:
    pass

if 'blackwidow.pipelines.DjangoModelPipeline' in ITEM_PIPELINES:
    setup_django_env(DJANGO_SETTINGS_DIR)
