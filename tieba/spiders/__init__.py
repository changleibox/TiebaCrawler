# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from tieba.spiders.auto_post_spiders import AutoPostSpider
from tieba.spiders.auto_sign_spiders import AutoSignSpider

AutoSignSpider = AutoSignSpider
AutoPostSpider = AutoPostSpider
