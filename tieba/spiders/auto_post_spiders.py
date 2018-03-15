#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/3/7.
import json
import re
import time

from tieba import utils
from tieba.common.configs import *
from tieba.post.post import InputPost
from tieba.spiders.index_spiders import IndexSpider


# noinspection PyMethodMayBeStatic
class AutoPostSpider(IndexSpider):
    name = 'AutoPost'

    def __init__(self, name=None, **kwargs):
        super(AutoPostSpider, self).__init__(name, **kwargs)
        self.kw = None
        self.fid = 0
        self.post_datas = None

    def parse_index_response(self, response):
        self.kw = raw_input('请输入贴吧名字：')
        self.post_datas = InputPost(self.kw)
        return [self.__get_teiba_datas(kw=self.kw)]

    def parse_tieba_datas(self, response):
        text = response.body.replace('\r', '').replace('\n', '').strip()
        text_re = re.search(r'PageData\.forum = {(.*?)};', text)
        if text_re:
            tieba_json_str = '{%s}' % text_re.group(1)
            tieba_json_str = re.compile(r'/\*.*?\*/', re.I).sub('', tieba_json_str.replace('\'', '\"'))
            utils.debug('贴吧信息：', tieba_json_str)
            tieba_json_obj = json.loads(tieba_json_str)
            self.fid = tieba_json_obj['id']
            self.kw = tieba_json_obj['name']
            yield self.post_note_or_reply()
        else:
            self.kw = raw_input('请输入贴吧名字：')
            self.post_datas = InputPost(self.kw)
            yield self.__get_teiba_datas(kw=self.kw)

    def parse_check_captcha(self, response):
        no = int(json.loads(response.body)['anti_valve_err_no'])
        utils.debug('验证码正确' if no == 0 else '验证码错误')

    def parse_post_note(self, response):
        json_obj = json.loads(response.body)
        no = int(json_obj['no'])
        if no == 0:
            utils.debug('发帖成功：', json.dumps(json_obj['data']))
            tid = json_obj['data']['tid']

            time.sleep(2)
            yield self.post_reply(tid)
        else:
            err_code = int(json_obj['err_code'])
            utils.debug('发帖失败：', get_post_err_msg(no, err_code, response.body))
        if no == 40:
            vcode_obj = json_obj['data']['vcode']
            input_captcha = utils.show_captcha(vcode_obj['captcha_vcode_str'])
            captcha_type = vcode_obj['captcha_code_type']
            yield self.__check_captcha(captcha=input_captcha, captcha_type=captcha_type)

            yield self.post_note(input_captcha)

    def parse_post_reply(self, response):
        json_obj = json.loads(response.body)
        no = int(json_obj['no'])
        data_obj = json_obj['data']
        tid = int(data_obj['tid']) if 'tid' in data_obj else 0
        if no == 0 and tid != 0:
            utils.debug('评论成功：', json.dumps(json_obj['data']))

            time.sleep(60)
            yield self.post_reply(tid)
        else:
            err_code = int(json_obj['err_code'])
            utils.debug('评论失败：', get_post_err_msg(no, err_code, response.body))
        if no == 220034 and tid != 0:
            time.sleep(300)
            yield self.post_reply(tid)
        if no == 40 and tid != 0:
            vcode_obj = json_obj['data']['vcode']
            input_captcha = utils.show_captcha(vcode_obj['captcha_vcode_str'])
            captcha_type = vcode_obj['captcha_code_type']
            yield self.__check_captcha(captcha=input_captcha, captcha_type=captcha_type)

            yield self.post_reply(tid, input_captcha)

    def post_note_or_reply(self):
        input_value = input('输入1发帖，输入2顶贴：')
        if input_value == 1:
            return self.post_note()
        elif input_value == 2:
            return self.post_reply(None)
        else:
            return self.post_note_or_reply()

    def post_note(self, captcha=''):
        title, content = self.post_datas.get_note(captcha)
        return self.__post_note(self.tbs, title[:MAX_TITLE], content[-MAX_CONTENT:], self.fid, self.kw, captcha)

    def post_reply(self, tid, captcha=''):
        tid = raw_input('请输入帖子Id：') if tid is None or len(str(tid)) == 0 else tid
        reply = self.post_datas.get_reply(captcha)
        return self.__post_reply(tid, self.tbs, reply[-MAX_REPLY:], self.fid, self.kw, captcha)

    def __get_teiba_datas(self, kw=DEFAULT_KW):
        datas = {
            'kw': kw,
            'fr': 'index'
        }
        return self._get(URL_BAIDU_INDEX + 'f', HEADERS, datas, self.parse_tieba_datas)

    def __check_captcha(self, captcha, captcha_type):
        headers = HEADERS.copy()
        headers['Referer'] = 'https://tieba.baidu.com/f?kw=%s&fr=home' % self.kw
        datas = {
            'fid': self.fid,
            'captcha_input_str': captcha,
            'captcha_code_type': str(captcha_type),
            'captcha_vcode_str': utils.md5(captcha)
        }
        return self._post(URL_BAIDU_INDEX + 'f/commit/commonapi/checkVcode', headers, datas, self.parse_check_captcha)

    def __post_note(self, tbs, title, content, fid, kw, captcha=''):
        mouse_pwd_t, mouse_pwd = self.__get_mouse_pwd()
        headers = HEADERS.copy()
        headers['Referer'] = 'https://tieba.baidu.com/f?kw=%s&fr=home' % kw
        datas = {
            'ie': 'utf-8',
            'kw': kw,
            'fid': str(fid),
            'tid': '0',
            'vcode': captcha,
            'vcode_md5': '' if captcha == '' else utils.md5(captcha),
            'floor_num': '0',
            'rich_text': '1',
            'tbs': tbs,
            'content': content,
            'basilisk': '1',
            'title': title,
            'prefix': '',
            'mouse_pwd': mouse_pwd,
            'mouse_pwd_t': mouse_pwd_t,
            'mouse_pwd_isclick': '0',
            '__type__': 'thread',
            '_BSK': self.__get_bsk(tbs)
        }
        return self._post(URL_BAIDU_INDEX + 'f/commit/thread/add', headers, datas, self.parse_post_note)

    def __post_reply(self, tid, tbs, content, fid, kw, captcha=''):
        mouse_pwd_t, mouse_pwd = self.__get_mouse_pwd()
        headers = HEADERS.copy()
        headers['Referer'] = 'http://tieba.baidu.com/p/%s' % tid
        datas = {
            'ie': 'utf-8',
            'kw': kw,
            'fid': str(fid),
            'tid': str(tid),
            'vcode': captcha,
            'vcode_md5': '' if captcha == '' else utils.md5(captcha),
            'floor_num': '0',
            'rich_text': '1',
            'tbs': tbs,
            'content': content,
            'basilisk': '1',
            'files': [],
            'mouse_pwd': mouse_pwd,
            'mouse_pwd_t': mouse_pwd_t,
            'mouse_pwd_isclick': '0',
            '__type__': 'reply',
            '_BSK': self.__get_bsk(tbs)
        }
        return self._post(URL_BAIDU_INDEX + 'f/commit/post/add', headers, datas, self.parse_post_reply)

    @classmethod
    def __get_bsk(cls, tbs):
        return utils.runtime('./js/_bsk.js').call('solve_bsk', tbs)

    @classmethod
    def __get_mouse_pwd(cls):
        mouse_pwd_t = str(utils.timestamp)
        mouse_pwd_fix = '28,29,20,8,19,17,17,23,45,21,8,20,8,21,8,20,8,21,8,20,8,21,8,20,45,22,22,28,21,17,45,21,18,' \
                        '28,20,8,21,20,17,20,'
        mouse_pwd = mouse_pwd_fix + mouse_pwd_t + '0'
        return mouse_pwd_t, mouse_pwd
