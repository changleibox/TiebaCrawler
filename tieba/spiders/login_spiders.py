#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/3/7.
import abc
import base64
import json
import re

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from tieba import utils
from tieba.common.configs import *
from tieba.post.post import LoginPost
from tieba.spiders.base_spiders import BaseSpider


# noinspection PyUnusedLocal
class LoginSpider(BaseSpider):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name=None, **kwargs):
        super(LoginSpider, self).__init__(name, **kwargs)
        self.__username = None
        self.__password = None
        self.__token = None
        self.__pubkey = None
        self.__rsakey = None
        self.__code_string = None
        self.__login_post = LoginPost()

    def parse(self, response, **kwargs):
        pass

    @abc.abstractmethod
    def parse_login_success(self, response):
        return []

    def start_requests(self):
        return [self.__index()]

    def parse_index(self, response):
        yield self.__get_token()

    def parse_token(self, response):
        json_str = re.search(r'.*?\((.*)\)', response.body).group(1).replace('\'', '\"')
        utils.debug('获取Token：', json_str)
        data = json.loads(json_str)
        self.__token = data['data']['token']
        yield self.__get_rsa_key()

    def parse_public_key(self, response):
        json_str = re.search(r'.*?\((.*)\)', response.body).group(1).replace('\'', '\"')
        utils.debug('获取Publickey：', json_str)
        data = json.loads(json_str)
        self.__pubkey = data['pubkey']
        self.__rsakey = data['key']
        yield self.__monitor_captcha(self.__get_username())

    def parse_monitor_captcha(self, response):
        json_str = re.search(r'.*?\((.*)\)', response.body).group(1).replace('\'', '\"')
        utils.debug('验证码：', json_str)
        self.__code_string = json.loads(json_str)['codestring']
        if self.__code_string is None or self.__code_string == 'null':
            yield self.__login()
        else:
            yield self.__get_captcha(self.__code_string)

    def parse_get_captcha(self, response):
        input_captcha = utils.show_captcha(response.body)
        if input_captcha == '1':
            yield self.__get_captcha(self.__code_string)
        else:
            yield self.__login(self.__code_string, input_captcha)

    def parse_login(self, response):
        errno = int(re.search(r'err_no=(\d+)', response.text).group(1))
        self.__code_string = re.search(r'&codeString=(.*?)&', response.body).group(1)
        if errno == 0:
            self.__password = None
            utils.debug('登录成功')
            for request in self.parse_login_success(response):
                yield request
        else:
            utils.debug(get_login_err_msg(errno, response.body))
        if errno == 1 or errno == 2 or errno == 4 or errno == 53 or errno == 58:
            if errno == 1 or errno == 2 or errno == 53 or errno == 58:
                self.__username = None
                utils.set_account(username='')
            self.__password = None
            utils.set_account(password='')
            yield self.__login(self.__code_string)
        elif errno == 6 or errno == 257:
            yield self.__get_captcha(self.__code_string)
        else:
            self.__username = None
            self.__password = None

    def relogin(self):
        return self.__index()

    def __index(self):
        return self._get(URL_BAIDU_INDEX, HEADERS, None, self.parse_index)

    def __get_token(self):
        datas = {
            'tpl': 'netdisk',
            'subpro': 'netdisk_web',
            'apiver': 'v3',
            'tt': str(utils.timestamp),
            'class': 'login',
            'gid': self._get_gid(),
            'logintype': 'basicLogin',
            'callback': self._get_callback()
        }
        headers = HEADERS.copy()
        headers.update(
            dict(Referer='http://tieba.baidu.com/', Accept='*/*', Connection='keep-alive', Host='passport.baidu.com'))
        return self._get(URL_BAIDU_TOKEN, headers, datas, self.parse_token)

    def __get_rsa_key(self):
        datas = {
            'token': self.__token,
            'tpl': 'netdisk',
            'subpro': 'netdisk_web',
            'apiver': 'v3',
            'tt': str(utils.timestamp),
            'gid': str(self._get_gid()),
            'callback': self._get_callback()
        }
        return self._get(URL_BAIDU_PUBLICKEY, HEADERS, datas, self.parse_public_key)

    def __monitor_captcha(self, username):
        datas = {
            'callback': self._get_callback(),
            'tpl': 'netdisk',
            'charset': 'utf-8',
            'index': '0',
            'username': username,
            'isphone': 'false',
            'time': str(utils.timestamp)
        }
        return self._get(URL_BAIDU_MONITOR_CAPTCHA, HEADERS, datas, self.parse_monitor_captcha)

    def __get_captcha(self, code_string):
        datas = {
            'v': str(utils.timestamp)
        }
        return self._get(URL_BAIDU_GET_CAPTCHA + code_string, HEADERS, datas, self.parse_get_captcha)

    def __login(self, codestring='', captcha=''):
        username = self.__get_username()
        password = self.__get_password()
        password = self.encript_password(password, self.__pubkey)
        datas = self.__get_login_datas(username, password, self.__rsakey, codestring, captcha)
        return self._post(URL_BAIDU_LOGIN, HEADERS, datas, self.parse_login)

    def __get_login_datas(self, username, password, rsakey, codestring='', captcha=''):
        return {
            'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'charset': 'utf-8',
            'token': self.__token,
            'tpl': 'netdisk',
            'subpro': 'netdisk_web',
            'apiver': 'v3',
            'tt': str(utils.timestamp),
            'codestring': codestring,
            'verifycode': captcha,
            'safeflg': '0',
            'u': '',
            'isPhone': '',
            'detect': '1',
            'gid': self._get_gid(),
            'quick_user': '0',
            'logintype': 'basicLogin',
            'logLoginType': 'pc_loginBasic',
            'idc': '',
            'loginmerge': 'true',
            'foreignusername': '',
            'username': username,
            'password': password,
            'mem_pass': 'on',
            # 返回的key
            'rsakey': rsakey,
            'crypttype': '12',
            'ppui_logintime': '33554',
            'countrycode': '',
            'callback': 'parent.' + self._get_callback()
        }

    def __get_username(self):
        if self.__username is None:
            self.__username = self.__login_post.get_username()
        return self.__username

    def __get_password(self):
        if self.__password is None:
            self.__password = self.__login_post.get_password()
        return self.__password

    @classmethod
    def _get_gid(cls):
        return utils.runtime('./js/login.js').call('getGid')

    @classmethod
    def _get_callback(cls):
        return utils.runtime('./js/login.js').call('getCallback')

    @classmethod
    def encript_password(cls, password, pubkey):
        """
        import rsa
        使用rsa库加密（法一）
        pub = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode('utf-8'))
        encript_passwd = rsa.encrypt(password.encode('utf-8'), pub)
        return base64.b64encode(encript_passwd).decode('utf-8')

        """
        # pubkey必须为bytes类型
        pub = RSA.importKey(pubkey.encode('utf-8'))
        # 构造“加密器”
        encryptor = PKCS1_v1_5.new(pub)
        # 加密的内容必须为bytes类型
        encript_passwd = encryptor.encrypt(password.encode('utf-8'))
        return base64.b64encode(encript_passwd).decode('utf-8')
