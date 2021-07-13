#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/3/2.
import abc
from abc import ABC
from urllib.parse import urlencode

import scrapy
from scrapy import Request, FormRequest
from scrapy.utils.python import to_bytes, is_listlike


def _urlencode(seq, enc='utf-8'):
    if seq:
        values = [(to_bytes(k, enc), to_bytes(v, enc))
                  for k, vs in seq
                  for v in (vs if is_listlike(vs) else [vs])]
        return urlencode(values, doseq=True)
    else:
        return ''


class BaseSpider(scrapy.Spider, ABC):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name=None, **kwargs):
        super(BaseSpider, self).__init__(name, **kwargs)
        self.cookies = None

    def _get(self, url, headers, body, callback=None, cookies=None, meta=None, errback=None):
        return NormalRequest(url=url, headers=headers, body=body, callback=callback, cookies=cookies or self.cookies,
                             meta=meta, errback=errback)

    def _put(self, url, headers, body, callback=None, cookies=None, meta=None, errback=None):
        return NormalRequest(url=url, headers=headers, body=body, callback=callback, method='PUT',
                             cookies=cookies or self.cookies, meta=meta, errback=errback)

    def _post(self, url, headers, formdata, callback=None, cookies=None, meta=None, errback=None):
        return FormRequest(url=url, headers=headers, formdata=formdata, callback=callback, dont_filter=True,
                           cookies=cookies or self.cookies, meta=meta, errback=errback)


class NormalRequest(Request):

    def __init__(self, url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None,
                 encoding='utf-8', priority=0, dont_filter=True, errback=None, flags=None):
        if method == 'POST':
            if body:
                items = body.items() if isinstance(body, dict) else body
                querystr = _urlencode(items, encoding)
                headers.setdefault(b'Content-Type', b'application/x-www-form-urlencoded')
                body = querystr
        elif method == 'GET':
            if body:
                items = body.items() if isinstance(body, dict) else body
                querystr = _urlencode(items, encoding)
                url = url + ('&' if '?' in url else '?') + querystr
                body = None
        elif method == 'PUT':
            if body:
                items = body.items() if isinstance(body, dict) else body
                body = _urlencode(items, encoding)
        super(NormalRequest, self).__init__(url, callback, method, headers, body, cookies, meta, encoding, priority,
                                            dont_filter, errback, flags)
