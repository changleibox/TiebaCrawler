# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from tieba import utils
from tieba.database.model import Forum
from tieba.utils import Logger

logger = Logger(__name__)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class TiebaPipeline(object):
    forum_model = Forum()

    def process_item(self, item, spider):
        forum = item['forum']
        forum['timestamp'] = utils.timestamp
        self.forum_model.add_datas(forum, True)
        logger.debug(json.dumps(forum), extra={'spider': spider})
        return item
