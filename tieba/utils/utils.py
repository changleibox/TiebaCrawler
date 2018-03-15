#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cStringIO
# Created by box on 2018/2/27.
import hashlib
import os

import execjs
import requests
import yaml
from PIL import Image


def get_configs(path_config=None):
    """获取 yaml 形式的配置文件内容.
    Note:
    + `path_config` 必须是配置文件的绝对路径
    """
    if not os.path.isabs(path_config):
        raise Exception('{0} should be absoule path.'.format(path_config))

    with open(path_config, 'r') as fp:
        configs = yaml.load(fp)

    return configs


def get_runntime(path):
    """
    :return: 编译后的js环境，不清楚pyexecjs这个库的用法的请在github上查看相关文档
    """
    phantom = execjs.get()  # 这里必须为phantomjs设置环境变量，否则可以写phantomjs的具体路径
    with open(path, 'r') as f:
        source = f.read()
    return phantom.compile(source)


def get_timestamp():
    import time
    return int(int(round(time.time() * 1000)))


def show_captcha(text):
    img_file = cStringIO.StringIO(text)
    img_file.seek(0)
    Image.open(img_file).show()
    return raw_input('请输入验证码，看不清按\'1\'：')


def md5(text):
    hl = hashlib.md5()
    hl.update(text.encode(encoding='utf-8'))
    return hl.hexdigest()


def get_img_size(url):
    try:
        data_stream = cStringIO.StringIO(requests.get(url).content)
        pil_image = Image.open(data_stream)
        return pil_image.size
    except IOError:
        return 0, 0


def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)  # 取文件绝对路径
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)


if __name__ == '__main__':
    print get_img_size('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec'
                       '=1520514352032&di=6c6c1814f318a15943154180a5f73474&imgtype=0&src=http%3A'
                       '%2F%2Fimg5.pcpop.com%2FArticleImages%2Ffnw%2F2016%2F1203%2F2ba3284b-2cf5'
                       '-4cfb-b495-8c0cae5a432a.jpg')
