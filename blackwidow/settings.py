# Scrapy settings for blackwidow project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'blackwidow'

SPIDER_MODULES = ['blackwidow.spiders']
NEWSPIDER_MODULE = 'blackwidow.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'blackwidow (+http://hello.com/)'

ITEM_PIPELINES = [
    'blackwidow.pipelines.NormalizationPipeline',
]
