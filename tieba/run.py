#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

# Created by box on 2018/3/7.
from scrapy import cmdline
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from tieba import spiders


def run_auto_sign():
    cmdline.execute('scrapy crawl AutoSign'.split())


def run_auto_post():
    cmdline.execute('scrapy crawl AutoPost'.split())


if __name__ == '__main__':
    # run_auto_sign()
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    runner.crawl(spiders.AutoSignSpider)
    # runner.crawl(spiders.AutoPostSpider)

    d = runner.join()
    # noinspection PyUnresolvedReferences
    d.addBoth(lambda _: reactor.stop())

    # blocks process so always keep as the last statement
    # noinspection PyUnresolvedReferences
    reactor.run()
    logging.info('all finished.')
