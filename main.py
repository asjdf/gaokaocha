from mirai import Mirai, Plain, MessageChain, Friend, Image, Group, protocol, Member, At, Face, JsonMessage,XmlMessage,LightApp
import asyncio
import requests
import io
from dotenv import load_dotenv
import os
import bs4
import time

def cha():
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            r = requests.get("http://gk.eeafj.cn/jsp/scores/gkcj/scores_enter.jsp")
            success = True
        except:
            attempts += 1
            print('超时了')
            time.sleep(2)
            return -1
    soup = bs4.BeautifulSoup(r.content.decode("utf-8"),"html.parser")
    print(r)
    print(soup.find(id="findbtn")["value"])
    answer = soup.find(id="findbtn")["value"]
    if answer == ' 成绩查询功能暂未开放 ':
        print('还没%s' %time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        return 0
    else:
        print('可查%s' %time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        return 1

# 加载环境变量
load_dotenv(verbose=True, override=True, encoding='utf-8')
qq = os.getenv('YOUR_QQ') # 字段 qq 的值
authKey = '1234567890' # 字段 authKey 的值
mirai_api_http_locate = '127.0.0.1:8080/' # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")
# 查分关键词
chafen = ['查分','可以查分了吗?','可以查分了吗','高考可以查分了吗?','高考可以查分了吗']
@app.receiver("FriendMessage")
async def event_gm(app: Mirai, friend: Friend, message: MessageChain):
    await app.sendFriendMessage(friend, [
        Plain(text="Hi,这是小b的QQ机器人,有问题找他")
    ])

@app.receiver("GroupMessage")
async def GMHandler(app: Mirai, group:Group, message:MessageChain, member:Member):
    print(message)
    sender=member.id
    groupId=group.id
    for keyWord in chafen:
        if message.toString() == keyWord:
            point = cha()
            if point == 0:
                await app.sendGroupMessage(group,[
                    Plain(text="还不行哦")
                ]) 
            elif point == 1:
                await app.sendGroupMessage(group,[
                    Plain(text="好像可以查了哦!去http://gk.eeafj.cn/jsp/scores/gkcj/scores_enter.jsp看看叭")
                ]) 
            elif point == -1:
                await app.sendGroupMessage(group,[
                    Plain(text="查询服务器爆满啦!不清楚能不能查.(链接超时)")
                ]) 

@app.subroutine
async def autoCha(app: Mirai):
    while True:
        await asyncio.sleep(1800)
        print("autoCha1:")
        cha1 = cha()
        print(cha)
        groupList = await app.groupList()
        for i in groupList:
        #     await app.sendGroupMessage(i,[
        #         Plain(text="爷来啦~")
        #     ])
            if cha1 == 0:
                await app.sendGroupMessage(i,[
                    Plain(text="高考成绩还不能查哦! -%s" %time.strftime('%H:%M:%S', time.localtime(time.time())))
                ]) 
            elif cha1 == 1:
                # await app.sendGroupMessage(i,[
                #     Plain(text="好像可以查了哦!去http://gk.eeafj.cn/jsp/scores/gkcj/scores_enter.jsp看看叭")
                # ]) 
                pass
            elif cha1 == -1:
                await app.sendGroupMessage(i,[
                    Plain(text="查询服务器爆满啦!不清楚能不能查.(链接超时)")
                ]) 

@app.subroutine
async def autoCha2(app: Mirai):
    while True:
        await asyncio.sleep(10)
        print("autoCha2:")
        cha1 = cha()
        print(cha)
        groupList = await app.groupList()
        for i in groupList:
        #     await app.sendGroupMessage(i,[
        #         Plain(text="爷来啦~")
        #     ])
            if cha1 == 0:
                # await app.sendGroupMessage(672989144,[
                #     Plain(text="高考成绩还不能查哦! -%s" %time.strftime('%H:%M:%S', time.localtime(time.time())))
                # ]) 
                pass
            elif cha1 == 1:
                await app.sendGroupMessage(i,[
                    Plain(text="好像可以查了哦!去http://gk.eeafj.cn/jsp/scores/gkcj/scores_enter.jsp看看叭")
                ]) 
            elif cha1 == -1:
                # await app.sendGroupMessage(i,[
                #     Plain(text="查询服务器爆满啦!不清楚能不能查.(链接超时)")
                # ]) 
                pass

if __name__ == "__main__":
    app.run()
    