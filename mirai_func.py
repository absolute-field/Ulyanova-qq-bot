from mirai import *
import requests
import json
import os
import base64
import random
import subprocess
import shlex
import urllib

from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.elements.internal import *
from graia.application.message.chain import MessageChain

import shlex
import asyncio
from mirai_func import *

from graia.application.friend import *
from graia.application.group import *

from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def Ohayo(app:Mirai , group: Group, member: Member, message: MessageChain):
    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Plain(text="早上好!")
        ])
    )

def hitokoto(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    hitokoto_instance = requests.get("https://v1.hitokoto.cn/?c=a&c=b&c=d&c=i&c=k").json()
    return app.sendGroupMessage(
        group.id,
        MessageChain.create([
            Plain(text=hitokoto_instance['from'] + ": " + hitokoto_instance['hitokoto'])
        ])
    )




def WangYiYun(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    r = requests.get("https://nd.2890.ltd/api/")
    data = json.loads(r.text)
    payload = data['data']['content']['content']
    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Plain(text=payload)
        ]
    ))


def TodayInHistory(app: GraiaMiraiApplication, group: Group, member: Member, message):
    r = requests.get("https://api.asilu.com/today")
    data = json.loads(r.text)
    payload = "今天是"+ data['month'] +"月"+data['day']+"日,在历史上的今天：\n"
    for i in data['data']:
        payload = payload + str(i['year']) + "年," + i['title'] +"\n"
    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Plain(text=payload)
        ]
    ))



def MindBoy(app: GraiaMiraiApplication, group: Group, member: Member, message):
    r = requests.get("https://api.66mz8.com/api/social.php?format=json")
    data = json.loads(r.text)
    payload = data['social']
    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Plain(text=payload)
        ]
    ))




def NetEaseMusic(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    msg_argv = message.asDisplay().split(" ", 1)
    SearchResult = requests.get(
        "https://musicapi.leanapp.cn/search?" + urllib.parse.urlencode({"keywords": msg_argv[1]}), timeout=3).json()['result']['songs'][0]
    SongId = SearchResult['id']
    SongName = SearchResult['name']
    ArtistName = '/'.join([x['name'] for x in SearchResult['artists']])
    CoverPic = requests.get("https://musicapi.leanapp.cn/song/detail?ids=" +
                            str(SongId), timeout=3).json()['songs'][0]['al']['picUrl']
    MusicUrl = "https://music.163.com/song/media/outer/url?id=" + str(SongId) + ".mp3"
    WebUrl = "https://music.163.com/#/song?id=" + str(SongId)

    finalXML = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="2" templateID="1" action="web" brief="[分享] {SongName}" sourceMsgId="0" url="{WebUrl}" flag="0" adverSign="0" multiMsgFlag="0"><item layout="2"><audio cover="{CoverPic}" src="{MusicUrl}" /><title>{SongName}</title><summary>{ArtistName}</summary></item><source name="网易云音乐" icon="https://s1.music.126.net/style/favicon.ico?v20180823" url="{WebUrl}" action="app" a_actionData="com.tencent.qqmusic" i_actionData="tencent1101079856://" appid="1101079856" /></msg>'''.format(
        SongName=SongName, WebUrl=WebUrl, CoverPic=CoverPic, MusicUrl=MusicUrl, ArtistName=ArtistName)
    # return app.sendGroupMessage(
    #     group.id,
    # MessageChain.create(
    #     [
    #         Plain(MusicUrl),
    #         Plain(SongName),
    #         Plain(str(SongId))
    #     ]
    # )

    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Plain(""),
            Xml(xml=finalXML)
        ]
    ))


def AnimePicCome(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    os.system("cd ./pic/;wget https://acg.yanwz.cn/api.php --no-check-certificate;mv api.php api.png")
    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Image.fromLocalFile("./pic/api.png")
        ]
    ))


def ahelp(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    payload = '''乌理扬诺娃换库辣！代码重写中.....
    目前已开启的的命令：
    #help: 打开帮助面板
    #一言: 一句经典的话,
    #网抑云: 网抑云语录,
    #历史上的今天: 历史上的今天发生了什么?,
    #精神小伙: 精神小伙语录,
    #网易云 (要点的歌曲): 网易云点歌
    #来点二次元 ：来个二次元图片
    #随机 (选项1)；(选项2)... ：选择困难症的好帮手！让机器人来帮你选了吧！
    #算卦 ：让机器人给你算一卦
    '''
    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Plain(payload)
        ]
    ))


def MakeaChoice(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    msg_argv = shlex.split(message.asDisplay())
    kw = ""
    try:
        kw = msg_argv[1]
    except:
        pass
    lst = kw.split("；")
    if "" in lst:
        lst.remove("")
    result = random.choice(lst)
    payload = "我的提议是"+str(result)+"，你看怎么样?"
    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Plain(payload)
        ]
    ))


def draw_lots(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    with open('./draw/draw_lots.json','rb') as json_f:
        json_load = json.load(json_f)
        gua = json_load["六十四卦"][random.randint(0,63)]
        payload = gua + "卦象解析如下：" + json_load[gua[-3:-1]][random.randint(0,len(json_load[gua[-3:-1]])-1)]
    return app.sendGroupMessage(
        group.id,
        MessageChain.create(
        [
            Plain(payload)
        ]
    ))
