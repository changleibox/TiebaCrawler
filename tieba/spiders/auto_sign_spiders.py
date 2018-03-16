#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/3/7.
import json
import re
import urllib
import urlparse
from time import sleep

from scrapy import Selector

from tieba import utils
from tieba.common.configs import *
from tieba.items import TiebaItem
from tieba.spiders.index_spiders import IndexSpider


# noinspection PyMethodMayBeStatic
class AutoSignSpider(IndexSpider):
    name = 'AutoSign'

    def __init__(self, name=None, **kwargs):
        super(AutoSignSpider, self).__init__(name, **kwargs)
        self.pn = 1
        self.forums = list()

    def parse_index_response(self, response):
        return [self.__onekey_signin(self.tbs)]

    def parse_onekey_signin(self, response):
        json_obj = json.loads(response.text)
        no = int(json_obj['no'])
        data = json_obj['data']
        if no == 0:
            utils.debug('签到成功：', json.dumps(data))
        else:
            error = data['str_reason'] if 'str_reason' in data else json_obj['error']
            utils.debug('签到失败：', error, strip=False)
        if no == 2150040:  # 此处为人机验证的验证码，没法整，先放着
            captcha_vcode_str = data['captcha_vcode_str']
            # captcha_vcode_type = data['captcha_code_type']
            input_captcha = '00010001000100000002000100020000'
            if input_captcha == '1':
                yield self.__onekey_signin(self.tbs)
            else:
                yield self.__onekey_signin(self.tbs, input_captcha, captcha_vcode_str)
        yield self.__get_my_forums()

    def parse_single_signin(self, response):
        json_obj = json.loads(response.text)
        no = int(json_obj['no'])
        data = json_obj['data']
        forum_name = urlparse.parse_qs(urllib.unquote(response.request.body))['kw'][0]
        tbs = urlparse.parse_qs(urllib.unquote(response.request.body))['tbs'][0]
        if no == 0:
            utils.debug('签到成功：', forum_name)
        else:
            error = data['str_reason'] if 'str_reason' in data else json_obj['error']
            utils.debug('签到失败：', error, '--->', forum_name, strip=False)
        if no == 2150040:  # 此处为人机验证的验证码，没法整，先放着
            captcha_vcode_str = data['captcha_vcode_str']
            # captcha_vcode_type = data['captcha_code_type']
            print captcha_vcode_str
            input_captcha = '00010001000100000002000100020000'
            if input_captcha == '1':
                yield self.__single_signin(tbs, forum_name)
            else:
                yield self.__single_signin(tbs, forum_name, input_captcha, captcha_vcode_str)

    def parse_my_forums(self, response):
        text = re.search(r'<table>(.*?)</table>', response.text).group(1)
        selector = Selector(text=text)
        trs = selector.xpath('//tr')
        if trs is not None and len(trs) > 1:
            trs = trs[1:]
            for tr in trs:
                if len(tr.xpath('td')) == 0:
                    continue
                forum = dict()
                forum['title'] = tr.xpath('td[1]/a/@title').extract()[0]
                forum['href'] = tr.xpath('td[1]/a/@href').extract()[0]
                forum['exper'] = tr.xpath('td[2]/a/text()').extract()[0]
                forum['fid'] = tr.xpath('td[4]/span/@balvid').extract()[0]
                forum['tbs'] = tr.xpath('td[4]/span/@tbs').extract()[0]
                self.forums.append(forum)

                item = TiebaItem(type=0)
                item['forum'] = forum
                yield item
            self.pn += 1
            yield self.__get_my_forums(pn=self.pn)
        else:
            index = 0
            for forum in self.forums:
                if index > 0:
                    sleep(2)
                index += 1
                yield self.__single_signin(forum['tbs'], forum['title'])

    def __onekey_signin(self, tbs, captcha_input_str=None, captcha_vcode_str=None):
        datas = {
            'ie': 'utf-8',
            'tbs': tbs,
            'captcha_input_str': '' if captcha_input_str is None else str(captcha_input_str),
            'captcha_vcode_str': '' if captcha_vcode_str is None else captcha_vcode_str
        }
        return self._post(URL_ONEKEY_SIGNIN, HEADERS, datas, self.parse_onekey_signin)

    def __single_signin(self, tbs, kw, captcha_input_str=None, captcha_vcode_str=None):
        datas = {
            'ie': 'utf-8',
            'tbs': tbs,
            'kw': kw,
            'captcha_input_str': '' if captcha_input_str is None else str(captcha_input_str),
            'captcha_vcode_str': '' if captcha_vcode_str is None else captcha_vcode_str
        }
        return self._post(URL_SINGLE_SIGNIN, HEADERS, datas, self.parse_single_signin)

    def __get_my_forums(self, pn=1):
        datas = {
            'v': str(utils.timestamp),
            'pn': str(pn),
        }
        return self._get(URL_BAIDU_INDEX + 'f/like/mylike', HEADERS, datas, self.parse_my_forums)
