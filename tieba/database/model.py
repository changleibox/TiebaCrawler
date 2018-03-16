#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/2/28.
from tieba.caches.location import DATABASE_USER_NAME, DATABASE_PASSWORD
from tieba.utils.mysql import Mysql, Model


class BaseModel(Model):
    _conn = Mysql(user=DATABASE_USER_NAME, passwd=DATABASE_PASSWORD, db='TiebaCrawler')


class Forum(BaseModel):
    _tbl = 'Forum'
