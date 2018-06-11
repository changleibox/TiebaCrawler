# 百度贴吧Crawler
实现百度贴吧的自动签到和自动发帖、自动回帖\
实现Cookies免登录

### Python版本
Python2.7

### 实现方式
主要是用了scrapy框架实现爬取，PIL实现现实验证码，运行前得先安装scrapy和PIL。\
scrapy安装方式 [scrapy入门教程](http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html)\
PIL使用教程[官网中文版](https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/00140767171357714f87a053a824ffd811d98a83b58ec13000)

### 运行方式
   运行这个文件 **run.py**或者用命令方式：
```commandline
scrapy crawl AutoSign
```
和
```commandline
scrapy crawl AutoPost
```
   
```python
import logging
    
from scrapy import cmdline
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from tieba import spiders


def run_auto_sign():
    cmdline.execute('scrapy crawl AutoSign'.split())


def run_auto_post():
    cmdline.execute('scrapy crawl AutoPost'.split())


if __name__ == '__main__':
    # run_auto_sign()
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    runner.crawl(spiders.AutoSignSpider)
    # runner.crawl(spiders.AutoPostSpider)

    d = runner.join()
    # noinspection PyUnresolvedReferences
    d.addBoth(lambda _: reactor.stop())

    # blocks process so always keep as the last statement
    # noinspection PyUnresolvedReferences
    reactor.run()
logging.info('all finished.')
```

### 未解决问题
签到和发帖、回复贴子的人机验证还未实现。

### 免责声明
```text
本项目所提供的信息和技术，只供参考之用。

其他人一概毋须以任何方式就任何信息传递或传送的失误、不准确或错误对用户或任何其他人士负任何直接或间接的责任。

任何人不得侵犯百度的任何合法权益，使用者应自行遵守百度相关的用户协议，不得爬取百度禁止的内容，否则责任自行
承担，本项目及项目提供者不承担任何直接或间接的责任。

在法律允许的范围内，本项目在此声明，不承担用户或任何人士就使用或未能使用本项目所提供的信息或任何链接或项目
所引致的任何直接、间接、附带、从属、特殊、惩罚性或惩戒性的损害赔偿（包括但不限于收益、预期利润的损失或失去
的业务、未实现预期的节省）。

本项目所提供的信息，若在任何司法管辖地区供任何人士使用或分发给任何人士时会违反该司法管辖地区的法律或条例的
规定或会导致本项目或其第三方代理人受限于该司法管辖地区内的任何监管规定时，则该等信息不宜在该司法管辖地区供
该等任何人士使用或分发给该等任何人士。用户须自行保证不会受限于任何限制或禁止用户使用或分发本项目所提供信息
的当地的规定。

本项目图片，文字之类版权申明，因为项目可以由用户自行下载修改，本项目无法鉴别所上传图片或文字的知识版权，如
果侵犯，请及时通知我们，本项目将在第一时间及时删除。

凡以任何方式下载使用本项目或直接、间接使用本项目资料者，视为自愿接受本项目声明的约束。
```

### License
```Copyright
Copyright © 2017 CHANGLEI. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```