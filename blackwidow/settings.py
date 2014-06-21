# Scrapy settings for blackwidow project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os


# BOT_NAME = 'BlackWidow'
# WEBSITE = 'heelsfetishism.com'
# USER_AGENT = '%s/2.0 (%s)' % (BOT_NAME, WEBSITE)
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'

SPIDER_MODULES = ['blackwidow.spiders', ]
NEWSPIDER_MODULE = 'blackwidow.spiders'

DEFAULT_ITEM_CLASS = 'blackwidow.items.HeelsItem'

LOG_LEVEL = 'DEBUG'

# set False to print to stdout
LOG_STDOUT = False

# FEED_FORMAT = 'json'
# FEED_URI = 'result.json'

COOKIES_ENABLED = True

CONCURRENT_REQUESTS = 6

ITEM_PIPELINES = {
    'blackwidow.pipelines.DefaultValuePipeline': 100,
    'blackwidow.pipelines.DuplicatePipeline': 200,
    'blackwidow.pipelines.NormalizationPipeline': 300,
    'blackwidow.pipelines.SubmitItemPipeline': 400,
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 500,
}

# http://doc.scrapy.org/en/latest/topics/images.html
if 'scrapy.contrib.pipeline.images.ImagesPipeline' in ITEM_PIPELINES.keys():
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    IMAGES_STORE = os.path.join(PROJECT_PATH, 'images')
    IMAGES_MIN_WIDTH = 450

try:
    from settings_prod import *
except ImportError:
    pass
