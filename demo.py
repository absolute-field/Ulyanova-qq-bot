from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.elements.internal import At, Plain
from graia.application.message.chain import MessageChain

import shlex
import asyncio
from mirai import *
from mirai_func import *

from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend
from graia.application.group import Group, Member

loop = asyncio.get_event_loop()

qq = 3278069650  # 字段 qq 的值
authKey = '848951521556'  # 字段 authKey 的值
mirai_api_http_locate = 'http://localhost:64724/'
local_api_addr = "127.0.0.1"
local_api_port = 8520

groupJoined = [1130621413, 530480686, 942265728]

funcDict = {'#ohayo': Ohayo,'#一言': hitokoto, "#网抑云": WangYiYun, "#历史上的今天":TodayInHistory, 
    "#精神小伙":MindBoy, "#网易云":NetEaseMusic, "网易云": ahelp, "网抑云": ahelp, "#help": ahelp,
    "#来点二次元": AnimePicCome,"#随机":MakeaChoice, "#算卦": draw_lots
    }


bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=mirai_api_http_locate, # 填入 httpapi 服务运行的地址
        authKey=authKey, # 填入 authKey
        account=qq, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
if __name__ == "__main__":
    @bcc.receiver("GroupMessage")
    async def group_message_listener(app: GraiaMiraiApplication,group:Group,member:Member,message:MessageChain):
        msg_argv = shlex.split(message.asDisplay())
        while msg_argv[0].startswith("@") or msg_argv[0].strip() == "":
            msg_argv.pop(0)
        if group.id in groupJoined:
            try:                 
                print(msg_argv[0])
                await funcDict[msg_argv[0]](app, group, member, message)
            except Exception as e:
                print(e)

app.launch_blocking()