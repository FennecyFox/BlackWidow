# Scrapy settings for blackwidow project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'BlackWidow'
BOT_VERSION = '1.0'
WEBSITE = 'http://heelsfetishism.com'
USER_AGENT = '%s/%s (+%s)' % (BOT_NAME, BOT_VERSION, WEBSITE)
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

SPIDER_MODULES = ['blackwidow.spiders']
NEWSPIDER_MODULE = 'blackwidow.spiders'

DEFAULT_ITEM_CLASS = 'blackwidow.items.HeelsItem'

ITEM_PIPELINES = [
    'blackwidow.pipelines.DuplicatePipeline',
    'blackwidow.pipelines.NormalizationPipeline',
    'scrapy.contrib.pipeline.images.ImagesPipeline',
]

# http://doc.scrapy.org/en/latest/topics/images.html
IMAGES_STORE = '/Users/vinta/Projects/blackwidow/images'
IMAGES_MIN_WIDTH = 400

# http://doc.scrapy.org/en/latest/topics/feed-exports.html
# store result in file
FEED_FORMAT = 'json'
FEED_URI = 'result.json'
