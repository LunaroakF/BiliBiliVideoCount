import requests as req
from time import strftime, localtime
import threading
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


BAV='4093721'
IsBV=False
sleepalltime=5


BVBV=BAV

RST = None 
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
mainroad='Fonts/'#'/home/pi/Documents/Programs/OLEDPrograms/Fonts/'
retron=mainroad+'Retron2000.ttf'
hanzi=mainroad+'Dengl.ttf'
NowTimes=""
AllTimes=""
padding=-2
top = padding
x=0
maindate=time.strftime('%Y-%m-%d',time.localtime(time.time()))
maintime=time.strftime('%H:%M:%S',time.localtime(time.time()))

view=''
danmaku=''
reply=''
coin=''
AVD=''
like=''
Rview=''
Rdanmaku=''
Rreply=''
Rcoin=''
Rlike=''



def get(AV):
    global view
    global AVD
    global danmaku
    global reply
    global coin
    global like
    global Rview
    global Rdanmaku
    global Rreply
    global Rcoin
    global Rlike
    url = "http://api.bilibili.com/archive_stat/stat?aid="+AV+ "&jsonp=jsonp"
    resp = req.get(url)
    info = eval(resp.text)
    AVD=AV
    info=info['data']
    like=info['like']
    view=info['view']
    danmaku=info['danmaku']
    reply=info['reply']
    coin=info['coin']
    Rview=str(view)
    Rdanmaku=str(danmaku)
    Rreply=str(reply)
    Rcoin=str(coin)
    Rlike=str(like)
    if like>=10000:
        Rlike=format(like/10000, '.1f')+"万"
    if coin>=10000:
        Rcoin=format(coin/10000, '.1f')+"万"
    if reply>=10000:
        Rreply=format(reply/10000, '.1f')+"万"
    if danmaku>=10000:
        Rdanmaku=format(danmaku/10000, '.1f')+"万"
    if view>=10000:
        Rview=format(view/10000, '.1f')+"万"
        
#算法来自知乎https://www.zhihu.com/question/381784377/answer/1099438784
table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
    tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

def dec(x):
    r=0
    for i in range(6):
        r+=tr[x[s[i]]]*58**i
    return (r-add)^xor

def enc(x):
    x=(x^xor)+add
    r=list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]]=table[x//58**i%58]
    return ''.join(r)


if IsBV:
    BAV=str(dec(BAV))
    print(BAV)

    #debug()

def Timeupdate():
    print("时钟已加载")
    while True:
        global maindate
        global maintime
        maindate=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        maintime=time.strftime('%H:%M:%S',time.localtime(time.time()))

def ScreenUpdate():
    while True:
        global maindate
        global maintime
        global NowTimes
        global AllTimes
        global MusicName
        global Replay
        global page
        global IsBV
        global BVBV
        last=1
        if page==1:
            if last!=1:
                disp.clear()
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x+85, top),maintime,  font=ImageFont.truetype(hanzi,12), fill=255)
            draw.text((x, top),maindate,  font=ImageFont.truetype(hanzi,12), fill=255)
            if IsBV:
                draw.text((x+2, top+13),'BV号:'+str(BVBV),  font=ImageFont.truetype(hanzi,14), fill=255)
            else:
                draw.text((x+2, top+13),'AV号:'+str(AVD),  font=ImageFont.truetype(hanzi,15), fill=255)
            draw.text((x+1, top+28),'点赞:'+Rlike+'  +'+str(LSlike),  font=ImageFont.truetype(hanzi,15), fill=255)
            draw.text((x+1, top+43),'播放:'+Rview+'  +'+str(LSview),  font=ImageFont.truetype(hanzi,15), fill=255)
            draw.text((x+120, top+55),'1',  font=ImageFont.truetype(hanzi,10), fill=255)
            last=1
        elif page==2:
            if last!=2:
                disp.clear()
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x+85, top),maintime,  font=ImageFont.truetype(hanzi,12), fill=255)
            draw.text((x, top),maindate,  font=ImageFont.truetype(hanzi,12), fill=255)
            draw.text((x+2, top+13),'弹幕:'+Rdanmaku+'  +'+str(LSdanmaku),  font=ImageFont.truetype(hanzi,15), fill=255)
            draw.text((x+1, top+28),'评论:'+Rreply+'  +'+str(LSreply),  font=ImageFont.truetype(hanzi,15), fill=255)
            draw.text((x+1, top+43),'硬币:'+Rcoin+'  +'+str(LScoin),  font=ImageFont.truetype(hanzi,15), fill=255)
            draw.text((x+120, top+55),'2',  font=ImageFont.truetype(hanzi,10), fill=255)
            last=2
        disp.image(image)
        disp.display()
        
page=1
def change():
    times=0
    while True:
        global page
        global sleepalltime
        time.sleep(1)
        times=times+1
        if times>sleepalltime:
            if page==1:
                page=2
            elif page==2:
                page=1
            times=0
            
def debug():
    global AVD
    print('AV号：'+AVD)
    print('播放量：'+view)
    print('弹幕数：'+danmaku)
    print('回复数：'+reply)
    print('硬币数：'+coin)

def reload():
    global RCDview
    global RCDdanmaku
    global RCDreply
    global RCDcoin
    global RCDlike
    global LSview
    global LSdanmaku
    global LSreply
    global LScoin
    global LSlike
    while True:
        try:
            get(BAV)
        except:
            get(BAV)
        LSview=view-RCDview
        LSdanmaku=danmaku-RCDdanmaku
        LSreply=reply-RCDreply
        LScoin=coin-RCDcoin
        LSlike=like-RCDlike
        time.sleep(5)

get(BAV)
RCDview=view
RCDdanmaku=danmaku
RCDreply=reply
RCDcoin=coin
RCDlike=like

LSview=view-RCDview
LSdanmaku=danmaku-RCDdanmaku
LSreply=reply-RCDreply
LScoin=coin-RCDcoin
LSlike=like-RCDlike

t_Timeupdate = threading.Thread(target=Timeupdate)
t_reload = threading.Thread(target=reload)
t_ScreenUpdate = threading.Thread(target=ScreenUpdate)
t_change = threading.Thread(target=change)
t_change.start()
t_Timeupdate.start()
t_reload.start()
t_ScreenUpdate.start()