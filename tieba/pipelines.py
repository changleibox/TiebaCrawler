# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from tieba import utils
from tieba.database.model import *
from tieba.utils import Logger

logger = Logger(__name__)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class TiebaPipeline(object):
    forum_model = Forum()
    note_model = Note()
    reply_model = Reply()

    def process_item(self, item, spider):
        item_type = item['type']
        if item_type == 0:
            forum = item['forum']
            forum['timestamp'] = utils.timestamp
            self.forum_model.add_datas(forum, True)
            logger.debug(json.dumps(forum), extra={'spider': spider})
        elif item_type == 1:
            note = item['note']
            self.note_model.add_datas(note, True)
            logger.debug(json.dumps(note), extra={'spider': spider})
        elif item_type == 2:
            reply = item['reply']
            self.reply_model.add_datas(reply, True)
            logger.debug(json.dumps(reply), extra={'spider': spider})
        return item
