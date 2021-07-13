#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/3/9.
import abc
import json
import re

import requests

from tieba import utils, common


# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
def tuling(info):
    app_key = "8f72ff0fdc8f4ddba24ff573e2f8c52c"
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s" % (app_key, info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text']
    return answer


class BasePost(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, kw):
        super(BasePost, self).__init__()
        self.kw = kw

    @abc.abstractmethod
    def get_note(self, captcha=''):
        pass

    @abc.abstractmethod
    def get_reply(self, tid, captcha=''):
        pass

    @classmethod
    def _create_img(cls, url):
        w, h = utils.get_img_size(url)
        if w == 0 or h == 0:
            return None
        max_width = 550
        max_height = 336
        if w > max_width:
            h = h * max_width / w
            w = max_width
        if h > max_height:
            w = w * max_height / h
            h = max_height
        return '[img pic_type=1 width=%d height=%d]%s[/img]' % (w, h, url)

    @classmethod
    def _create_imgs(cls, urls=None):
        if urls is None or len(urls) == 0:
            return ''
        imgs = list()
        for url in urls:
            img = cls._create_img(url)
            if img:
                imgs.append(img)
        return '[br]'.join(imgs)


class TestPost(BasePost):
    img = 'https://imgsa.baidu.com/forum/pic/item/11dfa9ec8a1363279139d9f49a8fa0ec09fac725.jpg'
    title = '%s，一个来了就不想离开的地方'
    content = '%s，著名的古代水利工程都江堰，位于四川都江堰市城西，古时属都安县境而名为都安堰，宋元后称都江被誉为“独奇千古”的“镇川之宝” ' \
              '。两千年前，李冰父子面对桀骜不驯的岷江水，火攻玉垒化为离堆。鱼嘴堤分水、飞沙堰溢洪、宝瓶口引水，将逢雨必涝的西蜀平原，化作' \
              '了水旱从人，不知饥馑的天府之国。这项工程直到今天还在发挥着作用，被称为“活的水利博物馆”。是全世界至今为止年代最久、唯一留存' \
              '、以无坝引水为特征的宏大水利工程。[br]' \
              '一千八百多年前，道教创始人张陵看中了青城山的碧绿清幽，决定在此修炼道法。青城山的香火愈来愈盛，但道家修建的观宇与亭阁始终深' \
              '藏于密林之间，与四周的山林岩泉融为一体。[br]' \
              '独特的地理条件和生态环境造就了离堆锁峡、金堤夕照、雄关古道、玉垒仙都、寒潭伏龙、笮桥飞虹、玉女仙姿、岷山晓雪、宝瓶春晓等自' \
              '然景观，与二王庙、伏龙观、安澜索桥、城隍庙等古代建筑交相辉映，形成了山、水、城、林、堰、桥融为一体的独特风光，成为自然与文' \
              '化、人类与环境、水利工程与山水风光和谐融合、天人合一的千古奇观。具有极强的观赏性、生态性、特色性。[br]' \
              '主要景观[br]' \
              '都江堰水利工程[br]' \
              '都江堰水利工程充分利用当地西北高、东南低的地理条件，根据江河出山口处特殊的地形、水脉、水势，乘势利导，无坝引水，自流灌溉，' \
              '使堤防、分水、泄洪、排沙、控流相互依存，共为体系，保证了防洪、灌溉、水运和社会用水综合效益的充分发挥。都江堰建成后，成都平' \
              '原沃野千里，“水旱从人，不知饥馑，时无荒年，谓之天府”。四川的经济文化有很大发展。其最伟大之处是建堰两千多年来经久不衰，而且' \
              '发挥着愈来愈大的效益。都江堰的创建，以不破坏自然资源，充分利用自然资源为人类服务为前提，变害为利，使人、地、水三者高度协调' \
              '统一。[br]' \
              '都江堰渠首枢纽主要由鱼嘴、飞沙堰、宝瓶口三大主体工程构成。三者有机配合，相互制约，协调运行，引水灌田，分洪减灾，具有“分四六' \
              '，平潦旱”的功效。[br]' \
              '1、岷江鱼嘴分水工程[br]' \
              '鱼嘴分水堤又称“鱼嘴”，是都江堰的分水工程，因其形如鱼嘴而得名，它昂头于岷江江心，包括百丈堤、杩槎、金刚堤等一整套相互配合的' \
              '设施。其主要作用是把汹涌的岷江分成内外二江，西边叫外江，俗称“金马河”，是岷江正流，主要用于排洪；东边沿山脚的叫内江，是人工' \
              '引水渠道，主要用于灌溉。[br]' \
              '在古代，鱼嘴是以竹笼装卵石垒砌。由于它建筑在岷江冲出山口呈弯道环流的江心，冬春季江水较枯，水流经鱼嘴上面的弯道绕行，主流直' \
              '冲内江，内江进水量约6成，外江进水量约4成；夏秋季水位升高，水势不再受弯道制约，主流直冲外江，内、外江江水的比例自动颠倒：内' \
              '江进水量约4成，外江进水量约6成。这就利用地形，完美地解决了内江灌区冬春季枯水期农田用水以及人民生活用水的需要和夏秋季洪水期' \
              '的防涝问题。[br]' \
              '2、飞沙堰溢洪排沙工程[br]' \
              '飞沙堰溢洪道又称“泄洪道”，具有泻洪、排沙和调节水量的显著功能，故又叫它“飞沙堰”。 飞沙堰是都江堰三大件之一，看上去十分平凡' \
              '，其实它的功用非常之大，可以说是确保成都平原不受水灾的关键要害。飞沙堰的作用主要是当内江的水量超过宝瓶口流量上限时，多余的' \
              '水便从飞沙堰自行溢出；如遇特大洪水的非常情况，它还会自行溃堤，让大量江水回归岷江正流。飞沙堰的另一作用是“[br]' \
              '飞沙”，岷江从万山丛中急驰而来，挟着大量泥沙、石块，如果让它们顺内江而下，就会淤塞宝瓶口和灌区。 古时飞沙堰，是用竹笼卵石堆' \
              '砌的临时工程；如今已改用混凝土浇铸，以保一劳永逸的功效。[br]' \
              '3、宝瓶口引水工程[br]' \
              '宝瓶口起"节制闸"作用，能自动控制内江进水量，是湔山(今名灌口山、玉垒山)伸向岷江的长脊上凿开的一个口子，它是人工凿成控制内江' \
              '进水的咽喉，因它形似瓶口而功能奇持，故名宝瓶口。留在宝瓶口右边的山丘，因与其山体相离，故名离堆。离堆在开凿宝瓶口以前，是湔' \
              '山虎头岩的一部分。由于宝瓶口自然景观瑰丽，有“离堆锁峡”之称，属历史上著名的“灌阳十景”之一。[br]' \
              '二王庙[br]' \
              '二王庙位于岷江右岸的山坡上，前临都江堰，原为纪念蜀王的望帝祠，齐建武（公元494～498年）时改祀李冰父子，更名为“崇德祠”。宋' \
              '代（公元960～1279年）以后，李冰父子相继被皇帝敕封为王，故而后人称之为“二王庙”。庙内主殿分别供奉有李冰父子的塑像，并珍藏有' \
              '治水名言、诗人碑刻等。建筑群分布在都江堰渠首东岸，规模宏大，布局严谨，地极清幽。是庙宇和园林相结合的著名景区。占地约5万余平' \
              '方米，主建筑约1万平方米。二王庙分东、西两菀，东菀为园林区，西菀为殿宇区。全庙为木穿逗结构建筑，庙寺完全依靠自然地理环境，依' \
              '山取势，在建筑风格上不强调中轴对称。上下重叠交错。宏伟秀丽，环境幽美。[br]' \
              '伏龙观[br]' \
              '伏龙观位于离堆公园内。其下临深潭，传说因李冰治水时曾在这里降伏孽龙在离堆之下，故于北宋初年改祭李冰，取名“伏龙观”。现存殿宇' \
              '三重，前殿正中立有东汉时期（公元25～220年）所雕的李冰石像。殿内还有东汉堰工石像、唐代金仙和玉真公主在青城山修道时的遗物——' \
              '飞龙鼎。伏龙观又名老王庙、李公词、李公庙等。清同治五年(公元1866年)四川巡抚祟实以为：“于虽齐圣，不先父食。况以公之贤：又有' \
              '功于蜀，其施力程能固无待乎其子。今乃数典忘祖，于掩其父得无紊钦?”[br]' \
              '安澜索桥[br]' \
              '安澜索桥又名“安澜桥”、“夫妻桥”。位于都江堰鱼嘴之上，横跨内外两江，被誉为“中国古代五大桥梁”，是都江堰最具特征的景观。始建于' \
              '宋代以前，明末（公元17世纪）毁于战火。古名“珠浦桥”，宋淳化元年改“评事桥”，清嘉庆建新桥更名为“安澜桥”。原索桥以木排石墩承托' \
              '，用粗竹缆横挂江面，上铺木板为桥面，两旁以竹索为栏，全长约500米，现在的桥为钢索混凝土桩。[br]' \
              '索桥在四川西部地区起源较早。安澜索桥修建具体年代已不从所考，但据《华阳国志·蜀志》记载李冰“能笮”。《水经注·江水》载“涪江有' \
              '笮桥”，证明至少安澜桥的修建，不会晚于修筑都江堰的年代。笮，意为竹索，这是川西古代索桥的主要建筑材料，故安澜索桥又被称为竹' \
              '桥、绳桥、竹藤桥等。现在的桥为1974年重建，下移100多米，将竹索改为钢索，承托缆索的木桩桥墩改为混凝土桩。[br]' \
              '都江堰卧铁[br]' \
              '卧铁是埋在内江“凤栖窝”处的淘滩标准，也是内江每年维修清淘河床深浅的标志。相传李冰建堰时在内江河床下埋有石马，作为每年淘滩深' \
              '度的标准，后来演变为卧铁。现有四根卧铁分别是明朝万历四年、清同治三年、民国十六年和1994年埋下的。现在游客在离堆古园内喷泉处' \
              '能看到的这四根卧铁的复制品，其真品还埋在内江河床下。[br]' \
              '其他景点[br]' \
              '奎光塔 虹口景区 南桥 园明宫[br]' \
              '清溪园 都江堰城隍庙 玉垒关 离堆公园[br]' \
              '秦堰楼 玉垒山公园 掷笔槽 青城外山景区[br]' \
              '幸福大道 翠月湖 灵岩寺'

    def __init__(self, kw):
        super(TestPost, self).__init__(kw)
        self.title = self.title % self.kw
        self.content = self.content % self.kw

    def get_note(self, captcha=''):
        imgs_str = self._create_imgs([self.img])
        if imgs_str != '':
            self.content += imgs_str + common.symbol_wrap
        return self.title, self.content

    def get_reply(self, tid, captcha=''):
        return tuling(self.kw)


class InputPost(BasePost):

    def __init__(self, kw):
        super(InputPost, self).__init__(kw)
        self.reply = None

    def get_note(self, captcha=''):
        title = input('请输入标题：')
        return title, self.__convert_img(input('请输入内容，图片用imgs=["...","...","..."]格式：'))

    def get_reply(self, tid, captcha=''):
        if self.reply is None:
            self.reply = self.__convert_img(input('请输入评论，图片用imgs=["...","...","..."]格式：'))
        return self.reply

    def __convert_img(self, content):
        content = str(content)
        p = re.search(r'imgs=(.*)', content)
        if p is not None:
            img_info = p.group(1)
            content = str(content.replace('imgs=' + img_info, ''))
            imgs_str = str(self._create_imgs(json.loads(img_info)))
            if imgs_str != '':
                content += imgs_str + str(common.symbol_wrap)
        return content


# noinspection PyMethodMayBeStatic
class LoginPost(object):

    def get_username(self):
        username = utils.get_account()['username']
        if username:
            return username
        else:
            username = input('请输入账号：')
            utils.set_account(username=username)
        return username

    def get_password(self):
        username = utils.get_account()['username']
        password = utils.get_account()['password']
        if username and password:
            return password
        else:
            password = input('请输入密码：')
            utils.set_account(password=password)
        return password
