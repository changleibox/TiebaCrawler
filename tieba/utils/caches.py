#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/3/15.
import csv
import os

from tieba.common.configs import COOKIES_FILE_NAME, ACCOUNT_FILE_NAME
from tieba.utils import utils

__cookies = dict()


def read_request_cookies():
    global __cookies
    if os.path.exists(COOKIES_FILE_NAME):
        csv_reader = csv.reader(open(COOKIES_FILE_NAME, 'r'))
        for csv_field in csv_reader:
            __cookies[csv_field[0]] = csv_field[1]
        return __cookies if 'BDUSS' in __cookies and 'STOKEN' in __cookies else None


def set_request_cookies(request):
    global __cookies
    for c in request.headers.getlist('Cookie'):
        cookie_strs = str(c).split('; ')
        for cookie_str in cookie_strs:
            # 只缓存这两个字段就可以实现cookie登录
            if 'BDUSS' in cookie_str or 'STOKEN' in cookie_str:
                cookie_kv = cookie_str.split('=')
                __cookies[cookie_kv[0]] = cookie_kv[1]
    # 设定写入模式
    csv_writer = csv.writer(open(COOKIES_FILE_NAME, 'w'), dialect='excel')
    for key in __cookies.keys():
        # 写入具体内容
        csv_writer.writerow([key, __cookies[key]])


def clear_cookies():
    os.remove(COOKIES_FILE_NAME)


__account = {'username': None, 'password': None}


def get_account():
    global __account
    if os.path.exists(ACCOUNT_FILE_NAME):
        csv_reader = csv.reader(open(ACCOUNT_FILE_NAME, 'r'))
        for csv_field in csv_reader:
            __account[csv_field[0]] = csv_field[1]
    return __account


def set_account(username=None, password=None):
    if username:
        __account['username'] = username
    if password:
        __account['password'] = password
    # 设定写入模式
    csv_writer = csv.writer(open(ACCOUNT_FILE_NAME, 'w'), dialect='excel')
    for key in __account.keys():
        # 写入具体内容
        csv_writer.writerow([key, __account[key]])


def clear_account():
    if os.path.exists(ACCOUNT_FILE_NAME):
        os.remove(ACCOUNT_FILE_NAME)


def clear_caches():
    utils.del_file(os.path.join(os.path.abspath('..'), r'caches'))


if __name__ == '__main__':
    clear_caches()
