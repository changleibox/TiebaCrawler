#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/2/28.
import re

from tieba.utils import caches
from tieba.utils import utils
from tieba.utils.logger import Logger

timestamp = utils.get_timestamp()

logger = Logger(__name__)


def runtime(path):
    return utils.get_runntime(path)


def show_captcha(text):
    return utils.show_captcha(text)


def md5(text):
    return utils.md5(text)


def get_img_size(url):
    return utils.get_img_size(url)


# noinspection PyUnresolvedReferences
def debug(*args, **kwargs):
    # .decode('raw_unicode_escape')
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    out_msg = ''
    for arg in args:
        if arg is None:
            continue
        if isinstance(arg, unicode):
            arg = arg.encode('utf-8')
        if isinstance(arg, tuple):
            arg = ''.join(arg)
        out_msg += str(arg)
    unicodes = re.compile(r'[\s\w]+', re.I).findall(out_msg)
    for uni in unicodes:
        str_unicode = '\\' + uni
        try:
            r_str = str_unicode.decode('unicode_escape')
            out_msg = out_msg.replace(str_unicode, r_str)
        except UnicodeDecodeError:
            pass
    strip = kwargs['strip'] if 'strip' in kwargs else True
    wrap = kwargs['wrap'] if 'wrap' in kwargs else False
    if strip:
        out_msg = out_msg.replace(' ', '')
    if not wrap:
        out_msg = out_msg.replace('\n', '').replace('\r', '')
    logger.debug(out_msg)


def read_request_cookies():
    return caches.read_request_cookies()


def set_request_cookies(request):
    caches.set_request_cookies(request)


def get_account():
    return caches.get_account()


def set_account(username=None, password=None):
    caches.set_account(username, password)


def clear_account():
    caches.clear_account()
