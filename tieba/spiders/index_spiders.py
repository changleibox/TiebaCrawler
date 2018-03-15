#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/3/7.
import abc
import json
import re

from tieba import utils
from tieba.common.configs import URL_BAIDU_INDEX
from tieba.spiders.login_spiders import LoginSpider


class IndexSpider(LoginSpider):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name=None, **kwargs):
        super(IndexSpider, self).__init__(name, **kwargs)
        self.tbs = None
        self.user_info = None

    def start_requests(self):
        password = utils.get_account()['password']
        cookies = utils.read_request_cookies()
        if cookies and len(cookies) > 0 and password and len(password) > 0:
            return [self.__get_index(cookies)]
        else:
            return super(IndexSpider, self).start_requests()

    @abc.abstractmethod
    def parse_index_response(self, response):
        return []

    def parse_login_success(self, response):
        return [self.__get_index()]

    def parse_tieba_index(self, response):
        text = response.body.replace('\r', '').replace('\n', '').strip()
        user_json_str = '{%s}' % re.search(r'PageData\.user = {(.*?)};', text).group(1)
        user_json_str = re.compile(r'/\*.*?\*/', re.I).sub('', user_json_str.replace('\'', '\"'))
        utils.debug('用户信息：', user_json_str)
        self.user_info = json.loads(user_json_str)

        self.tbs = re.search(r'PageData\.tbs = "(.*?)";', response.body.strip()).group(1)

        for request in self.parse_index_response(response):
            yield request

    def __get_index(self, cookies=None):
        return self._get(URL_BAIDU_INDEX, None, None, self.parse_tieba_index, cookies=cookies)
