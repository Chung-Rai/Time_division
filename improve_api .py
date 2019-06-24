from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
from chatterbot import ChatBot 
from chatterbot.conversation import Statement
import os
import urllib
import json
import sys
import MySQLdb
from flask import Flask, render_template
from unidecode import unidecode
import pymysql
import html.parser
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
from urllib.parse import quote
import webbrowser
from time import sleep
import time
import requests

import jieba
from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from time import mktime
import base64
from requests import request
from pprint import pprint



app_id = '6ce16e8bf225487bb13dbedf540c26c5'
app_key = 'iL_dCVAjwX8Dz2HIT-oLVNzqJKg'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = '6ce16e8bf225487bb13dbedf540c26c5'
        self.app_key = 'iL_dCVAjwX8Dz2HIT-oLVNzqJKg'

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }



bot=ChatBot('Test')
"""
train_ubuntu = UbuntuCorpusTrainer(bot)
train_ubuntu.train()
"""
"""
file_trainer = ChatterBotCorpusTrainer(bot)
file_trainer.train(
    "./Documents/primary/files"
)
"""
"""
a=webbrowser.get('google-chrome')
a.open("http://localhost/test.html")
"""
def is_chinese(uchar):
    if '\u4e00' <=uchar<='\u9fff':
        return True
    else:
        return False

# 打开数据库连接
db = pymysql.connect("localhost","root","","UnityDB",charset="utf8" )
 
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

app = Flask(__name__)


@app.route("/chat/<string:id>/<string:say>", methods=['GET'])
def profile(id,say):

    sql = "INSERT INTO CHAT(NAME,SAY,id) \
      VALUES ('%s','%s','%s')" % ('YOU',say,id)

    cursor.execute(sql)
    db.commit() #存進sql
    #s1 =say
    
    for char in say:
       if(is_chinese(char)):
           flag=1
           break      
    if flag==1:
        say=say.replace('+','')
          
    
    else:
        response=bot.get_response(say)
        botsay=str(response)


    sql = "INSERT INTO CHAT(NAME,SAY,id) \
      VALUES ('%s','%s','%s')" % ('BOT',botsay,id)

    cursor.execute(sql)
    db.commit() #存進sql
    
    return botsay

@app.route("/insertmoney/<string:id>/<string:coin>", methods=['GET'])
def money(id,coin):
    content =  "SELECT * FROM registered \
    WHERE id ='%s'"%id
    cursor.execute(content)
    db.commit()
    # 获取所有记录列表 
    results = cursor.fetchall()
    for row in results: 
        c=row[3]  
    # 执行SQL语句
    coin=int(coin)
    coin+=c
    sql = "UPDATE registered SET Coin='%d' \
            WHERE id='%s'" % (coin,id)  
    cursor.execute(sql)
    db.commit()
    return "更新成功"

@app.route("/costmoney/<string:id>/<string:coin>", methods=['GET'])
def cosmoney(id,coin):
    content =  "SELECT * FROM registered \
    WHERE id ='%s'"%id
    cursor.execute(content)
    db.commit()
    # 获取所有记录列表 
    results = cursor.fetchall()
    for row in results: 
        c=row[3]  
    # 执行SQL语句
    coin=int(coin)
    coin=c-coin
    sql = "UPDATE registered SET Coin='%d' \
            WHERE id='%s'" % (coin,id)  
    cursor.execute(sql)
    db.commit()
    return "扣款成功"

@app.route("/getmoney/<string:id>", methods=['GET'])
def getmoney(id):
    # 执行SQL语句
    content =  "SELECT * FROM registered \
        WHERE id ='%s'"%id
    cursor.execute(content)
    db.commit()
    # 获取所有记录列表 
    results = cursor.fetchall()
    for row in results: 
        coin=row[3]  
    return str(coin)

@app.route("/contents/<string:id>", methods=['GET'])
def detail(id):
    # 执行SQL语句
    content =  "SELECT * FROM CHAT \
    WHERE id ='%s'"%id
    cursor.execute(content)
    db.commit()
    # 获取所有记录列表 
    results = cursor.fetchall()
    say=""
    for row in results: 
        say+=row[0]+":"+row[1]+"\n"   
    return say


@app.route("/registered/<string:id>/<string:pw>/<string:email>", methods=['GET'])
def registered(id,pw,email):
    x=0
    look="SELECT * FROM registered\
    WHERE id ='%s'"%id
    cursor.execute(look)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        x+=1
    if x>0:
        return ("帐号已经被注册过")
    else:
        sql = "INSERT INTO registered(id,pw,Email) \
        VALUES ('%s','%s','%s')" % (id,pw,email)
        cursor.execute(sql)
        db.commit() #存進sql
        return ("注册成功")
    

@app.route("/login/<string:id>/<string:pw>", methods=['GET'])
def login(id,pw):

    sql = "SELECT * FROM registered \
    WHERE id='%s'"%id
    sql +="AND pw='%s'"%pw
    try:
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        for row in  results:
            r1=row[0]
            r2=row[1]
        if r1 !=id:
            return ("this account isn't assit")
        else:
            return r1
    except:
        db.rollback()
        return "account or password wrong"


light_number1=['0','0','0','0','0','0','0','0','0','0','0','0']
previous_say=""
@app.route("/chat_ar/<string:f>/<string:say>", methods=['GET'])
def ar_chat(f,say):
 
    global event,say_time,song,local,address,search,previous_say,Departure_station,Destination_station

    if  f == "1" :

        say_time=say #新增时间
        if(conflict()=="1"):#若冲突时间
            botsay="4"
        elif(conflict()=="2"):
            botsay="抱歉已经超过时段了"
        else:
            if (say.find("点") < 0):
                botsay="14"
            else: 
                botsay="2"

    elif f=="14":
        if (say.find("点") < 0):
            botsay="很抱歉，我不清楚你的时间"
        else:
            say_time += say
            botsay="2"

    elif  f == "4" :
        if (say.find("好") >= 0) or (say.find("确定") >= 0) or (say.find("是") >= 0) or (say.find("恩") >= 0):
            botsay="2"
        else:
            botsay="好為你取消此行程"


    elif f == "2":
        event=say
        botsay="9"

    elif f == "9":
        if (say.find("好") >= 0) or (say.find("确定") >= 0) or (say.find("是") >= 0) or (say.find("恩") >= 0):
            Add_itinerary()
            botsay="好的已為你新增完毕"
        else:
            botsay="好為你取消此行程"

    elif f == "13":
        if (say.find("好") >= 0) or (say.find("确定") >= 0) or (say.find("是") >= 0) or (say.find("恩") >= 0):
            Delete_itinerary()
            botsay="好的已為你删除完毕"
        else:
            botsay="好為你取消此动作"
    


    elif f=="11":
        if (say.find("年") >= 0) or (say.find("月") >= 0) or (say.find("日") >= 0) or (say.find("点") >= 0) or (say.find("分") >= 0) or (say.find("星期") >= 0) :
            say_time=say
            botsay="13"
             
        else:
            say_time=""
            event=say
            botsay="13"



    elif f == "3":
        say_time=say
        Ad_clock()
        botsay = "好的"
    
    elif f == "5":
        song=say
        botsay=song_number()

    elif f == "10":
        say_time=say
        event=say
        botsay=itinerary()

    elif f == "17":
        if (say.find("1楼") >= 0) or (say.find("一楼") >= 0) or (say.find("2楼") >= 0) or (say.find("二楼") >= 0) :
            light_number=control_furniture("打开"+say)
        
        else:
            light_number=control_all_furniture("打开"+say)
        #a.open("file:///home/ray/Documents/primary/test.html"+"?id="+light_number)
        Add = "UPDATE `furniture_control` SET `number`='%s'"%(str(light_number))
        cursor.execute(Add)
        db.commit() #存進sql
        botsay="好的"

    elif f =="16":

        if (say.find("好") >= 0) or (say.find("确定") >= 0) or (say.find("是") >= 0) or (say.find("恩") >= 0):
            botsay="17"
        else:
            botsay="好的"

    elif f =="18":

        if (say.find("好") >= 0) or (say.find("确定") >= 0) or (say.find("是") >= 0) or (say.find("恩") >= 0):

            if (say.find("1楼") >= 0) or (say.find("一楼") >= 0) or (say.find("2楼") >= 0) or (say.find("二楼") >= 0) :
                light_number=control_furniture(say_contral_furniture)
        
            else:
                light_number=control_all_furniture(say_contral_furniture)

            Add = "UPDATE `furniture_control` SET `number`='%s'"%(str(light_number))
            cursor.execute(Add)
            db.commit() #存進sql
            botsay="好的"
            #say_contral_furniture=""
        else:
            botsay="好的"


    elif f =="19":
        response=bot.get_response(say)
        #botsay=str(response)
        if (say.find("乱说") >= 0) :

            botsay="好的"
        elif response == "None":
            botsay="很抱歉我还是不懂"
        else:
            previous_say = Statement(previous_say)
            bot.learn_response(response, previous_say)
            botsay="我懂了"+dialogue(str(response))
            previous_say=""

    elif f=="20":
        station = jieba.cut(say, cut_all=False)
        c = 0
        for s in station:
            if c==0:
                Departure_station = s
            else:
                Destination_station = s
            c+=1

        Departure_station=station_number(Departure_station)

        Destination_station=station_number(Destination_station)


        botsay ="21"

    elif f=="21":

        previous_word=""
        t_minute=0
        t_hour=0
        words = jieba.cut(say, cut_all=False)

        for word in words:
            if word =="月":
                month=get_int(previous_word)
                if int(month) < 10:
                    month='0'+previous_word
            elif word =="日" or word =="号":
                day=get_int(previous_word)
                if int(day) < 10:
                    day='0'+previous_word
            elif word =="点":
                t_hour=get_int(previous_word)       
                t_hour=int(t_hour)
                if say.find("下午")>=0 or say.find("晚上")>=0:
                    t_hour += 12
            elif word =="分":
                t_minute=get_int(previous_word)
                t_minute=int(t_minute)
                
            previous_word=word

        #print("2019-"+month+"-"+day)

        time="2019-"+month+"-"+day
        if train(t_hour,t_minute,time) !="":
            botsay =  train(t_hour,t_minute,time)
        else:
            botsay="很抱歉查无资料"
        
    elif (say.find("点") >= 0):
        say_time=say
        
        s_time()

        if(conflict()=="1"):#若冲突时间
            botsay="4"
        elif(conflict()=="2"):
            botsay="抱歉已经超过时段了"
        """
        words = jieba.cut(say, cut_all=True)
        
        c=[]
        name=""
        for word in words:
            if word in "朋友老师":
                name +=word
            c += [word]

        if name !="":
            event =  c[len(c)-1] +"("+name+")"
        else:
           
            event =  c[len(c)-1]
        """
        try:
            event = say.split('分',1)[1]
            botsay="9"
        except:
            botsay="很抱歉"

    elif (say.find("新增") >= 0) and (say.find("闹钟") >= 0) :
        if (say.find("点") >= 0) and (say.find("分") >= 0): 
            say_time=say
            Ad_clock()
            botsay="好的"
        else:
            botsay = "3"
    elif (say.find("新增") >= 0 or say.find("添加")>= 0) and ((say.find("行事历") >= 0) or (say.find("新势力") >= 0) or (say.find("行程") >= 0)):
        
        botsay = "1"

    elif (say.find("删除") >= 0) and ((say.find("行事历") >= 0) or (say.find("新势力") >= 0) or (say.find("行程") >= 0)):

        botsay = "11"

    elif ((say.find("行事历") >= 0) or (say.find("新势力") >= 0) or (say.find("行程") >= 0)):
        #say_time=say
        #botsay=itinerary()
        botsay="10"

    elif say.find("自我介绍") >= 0:

        botsay="我的名子是小白　是个聪明的人工智慧管家唷"

    elif say.find("天气") >= 0 :
        
        local=quote(say,'utf-8')
        html =requests.get('https://www.google.com.tw/search?q='+local)
        soup = BeautifulSoup(html.text,"html.parser")
        td = soup.find("span",class_="BNeawe tAd8D AP7Wnd").text

        
        if (str(td) == "None"):
            botsay="很抱歉"

        else:
            say_time =say
            address =td

            local = jieba.cut(address, cut_all=False)

            for c in local:
                local = c
                break
        botsay=weather(0)



    elif say.find("空气") >= 0 :
        s2=say.lower()
        s="空气"
        m=""
        for c in s2:
            if c  in s:
                pass
            else:
                m+=c
        m+="天气"
        local=quote(m,'utf-8')
        html =requests.get('https://www.google.com.tw/search?q='+local)
        soup = BeautifulSoup(html.text,"html.parser")
        td = soup.find("span",class_="BNeawe tAd8D AP7Wnd").text

        if (str(td) == "None"):
            botsay="很抱歉"

        else:
            
            say_time =say
            address =td

            local = jieba.cut(address, cut_all=False)

            for c in local:
                local = c
                break

            botsay=weather_air(local)

    elif (say.find("youtube") >= 0 or (say.find("音乐") >= 0) or (say.find("歌") >= 0) or say.find("YouTube") >= 0  or say.find("播放") >= 0 ):
        if say.find("搜寻") >= 0 or say.find("播放") >= 0 :
            s=say
            song=s.lstrip('youtube搜寻YouTube播放')
            botsay="6"
        else: 
            botsay="5"  
    
    elif (say.find("google") >= 0 or (say.find("上网搜寻") >= 0) or (say.find("什么是") >= 0)):
        s=say
        search=s.lstrip('google搜寻上网搜寻什么是')
        botsay="15"


    elif (say.find("开") >= 0 or say.find("关") >= 0)  and say.find("灯") >= 0 :
        #a=webbrowser.get('google-chrome')
        if (say.find("点") >= 0 or say.find("分") >= 0):
            say_time=say
            if s_time() == "OUT_TIME":
                return "超过时段了"
            if say.find("分") >= 0:
                event=say_time[say_time.find("分")+1:]
            else:
                event=say_time[say_time.find("点")+1:]
            Add_itinerary()
            botsay="好的"
        else:
            if (say.find("1楼") >= 0) or (say.find("一楼") >= 0) or (say.find("2楼") >= 0) or (say.find("二楼") >= 0) :
                light_number=control_furniture(say)
            
            else:
                light_number=control_all_furniture(say)
            #a.open("file:///home/ray/Documents/primary/test.html"+"?id="+light_number)
            Add = "UPDATE `furniture_control` SET `number`='%s'"%(str(light_number))
            cursor.execute(Add)
            db.commit() #存進sql
            botsay="好的"
        #os.system("pkill chrome")

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("关") >= 0 or say.find("开") >= 0 or say.find("關") >= 0 or say.find("開") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/openTV.html")
        botsay="好的" 
        #os.system("pkill chrome")
    
        
    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("前") >= 0 or say.find("前") >= 0) and (say.find("頻道") >= 0 or say.find("频道") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/AddChannel.html")
        botsay="好的" 
        #os.system("pkill chrome")

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("後") >= 0 or say.find("後") >= 0) and (say.find("頻道") >= 0 or say.find("频道") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/decreasechannel.html")
        botsay="好的" 
        #os.system("pkill chrome")

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("頻道") >= 0 or say.find("频道") >= 0 or (say.find("台") >= 0 or say.find("台") >= 0)) :

        s2=say.lower()
        s1="十九八七六五四三二一" 
        s3="0123456789"
        m=""
        for c in s2:
            if c  in s1:
                c = chinese_number(c)
                m+=c
            elif c in s3:
                m+=c
        
        chanel = m
        botsay="好的已經為您切至"+chanel+"頻道"
        #chanel = int(chanel)
        #chanel_ten = int(chanel / 10)
        #chanel_one = chanel % 10
        #chanel_signal(chanel_ten)
        #chanel_signal(chanel_one)
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/TVchannel.html"+"?id="+chanel)

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("增加") >= 0 or say.find("增加") >= 0 or say.find("大聲") >= 0 or say.find("大声")) and (say.find("音量") >= 0 or say.find("音量") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/AddTVshound.html")
        botsay="好的" 
        #os.system("pkill chrome")

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("減少") >= 0 or say.find("减少") >= 0 or say.find("小聲") >= 0) or say.find("小声") and (say.find("音量") >= 0 or say.find("音量") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/decreaseTVshound.html")
        botsay="好的" 
        #os.system("pkill chrome")

    elif (say.find("跟对方问好") >= 0 or say.find("跟對方問好") >= 0):
        botsay="7"
        


    elif (say.find("玩游戏") >= 0 or say.find("运动") >= 0 or say.find("玩遊戲") >= 0 or say.find("運動") >= 0):
        botsay="8"

    elif say.find("火车") >= 0 :
        botsay="20"

    else:
        response=bot.get_response(say)
        #response=bot.generate_response(say)
        #botsay=str(response)
        if response == "None":
            previous_say=Statement(say)

            for preprocessor in bot.preprocessors:
                previous_say = preprocessor(previous_say)
            previous_statement = bot.get_latest_response(previous_say.conversation)
            bot.learn_response(previous_say, previous_statement)

            botsay ="19"
        else:
            botsay=dialogue(str(response))

 
    
    return botsay

def dialogue(say):
    global event,say_time,song,local,address,search,say_contral_furniture

    if (say.find("新增") >= 0) and (say.find("闹钟") >= 0) :
        if (say.find("点") >= 0) and (say.find("分") >= 0): 
            say_time=say
            Ad_clock()
            botsay="好的"
        else:
            botsay = "3"
    elif (say.find("新增") >= 0 or say.find("添加")>= 0) and ((say.find("行事历") >= 0) or (say.find("新势力") >= 0) or (say.find("行程") >= 0)):
        
        botsay = "1"

    elif (say.find("删除") >= 0) and ((say.find("行事历") >= 0) or (say.find("新势力") >= 0) or (say.find("行程") >= 0)):

        botsay = "11"

    elif ((say.find("行事历") >= 0) or (say.find("新势力") >= 0) or (say.find("行程") >= 0)):
        say_time=say
        botsay=itinerary()
        #botsay="10"

    elif ((say.find("自我介绍") >= 0) or (say.find("你叫什么名子") >= 0)):

        botsay="我的名子是小白　是个聪明的人工智慧管家唷"

    elif say.find("天气") >= 0 :
        
        local=quote(say,'utf-8')
        html =requests.get('https://www.google.com.tw/search?q='+local)
        soup = BeautifulSoup(html.text,"html.parser")
        td = soup.find("span",class_="BNeawe tAd8D AP7Wnd").text

        
        if (str(td) == "None"):
            botsay="很抱歉"

        else:
            say_time =say
            address =td

            local = jieba.cut(address, cut_all=False)

            for c in local:
                local = c
                break
        botsay=weather(0)

    elif say.find("空气") >= 0 :

        botsay=weather_air(say)

    elif (say.find("youtube") >= 0 or (say.find("音乐") >= 0) or (say.find("歌") >= 0) or say.find("YouTube") >= 0 ):
        if say.find("搜寻") >= 0 :
            s=say
            song=s.lstrip('youtube搜寻YouTube')
            botsay="6"
        else: 
            botsay="5"  
    
    elif (say.find("google") >= 0 or (say.find("上网搜寻") >= 0) or (say.find("什么是") >= 0)):
        s=say
        search=s.lstrip('google搜寻上网搜寻什么是')
        botsay="15"


    elif (say.find("开") >= 0 or say.find("关") >= 0)  and say.find("灯") >= 0 :
        #a=webbrowser.get('google-chrome')
        if say.find("客厅") >= 0 or say.find("阳台") >= 0 or say.find("楼梯")>= 0 or say.find("房间") >= 0 or say.find("厨房") >= 0 or say.find("全部") >= 0:
            say_contral_furniture =say
            if say.find("开") >= 0 :
                botsay = "18"
            if say.find("关") >= 0:
                botsay = "好的,路上小心唷"
                Add = "UPDATE `furniture_control` SET `number`='%s'"%(str(000000000000))
                cursor.execute(Add)
                db.commit() #存進sql
        else:
            botsay ="16"
        """
        if say.find("楼") >= 0 :
            light_number=control_furniture(say)
        
        else:
            light_number=control_all_furniture(say)
        #a.open("file:///home/ray/Documents/primary/test.html"+"?id="+light_number)
        Add = "UPDATE `furniture_control` SET `number`='%s'"%(str(light_number))
        cursor.execute(Add)
        db.commit() #存進sql
        botsay="好的"
        """
        #os.system("pkill chrome")

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("关") >= 0 or say.find("开") >= 0 or say.find("關") >= 0 or say.find("開") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/openTV.html")
        botsay="好的" 
        #os.system("pkill chrome")
    
        
    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("前") >= 0 or say.find("前") >= 0) and (say.find("頻道") >= 0 or say.find("频道") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/AddChannel.html")
        botsay="好的" 
        #os.system("pkill chrome")

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("後") >= 0 or say.find("後") >= 0) and (say.find("頻道") >= 0 or say.find("频道") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/decreasechannel.html")
        botsay="好的" 
        #os.system("pkill chrome")

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("頻道") >= 0 or say.find("频道") >= 0 or (say.find("台") >= 0 or say.find("台") >= 0)) :

        s2=say.lower()
        s1="十九八七六五四三二一" 
        s3="0123456789"
        m=""
        for c in s2:
            if c  in s1:
                c = chinese_number(c)
                m+=c
            elif c in s3:
                m+=c
        
        chanel = m
        botsay="好的已經為您切至"+chanel+"頻道"
        #chanel = int(chanel)
        #chanel_ten = int(chanel / 10)
        #chanel_one = chanel % 10
        #chanel_signal(chanel_ten)
        #chanel_signal(chanel_one)
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/TVchannel.html"+"?id="+chanel)

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("增加") >= 0 or say.find("增加") >= 0 or say.find("大聲") >= 0 or say.find("大声")) and (say.find("音量") >= 0 or say.find("音量") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/AddTVshound.html")
        botsay="好的" 
        #os.system("pkill chrome")

    elif (say.find("電視") >= 0 or say.find("电视") >= 0) and (say.find("減少") >= 0 or say.find("减少") >= 0 or say.find("小聲") >= 0) or say.find("小声") and (say.find("音量") >= 0 or say.find("音量") >= 0):
        a=webbrowser.get('google-chrome')
        a.open("file:///home/ray/Documents/primary/TVcontrol/decreaseTVshound.html")
        botsay="好的" 
        #os.system("pkill chrome")

    elif (say.find("跟对方问好") >= 0 or say.find("跟對方問好") >= 0):
        botsay="7"

    elif (say.find("玩游戏") >= 0 or say.find("运动") >= 0 or say.find("玩遊戲") >= 0 or say.find("運動") >= 0):
        botsay="8"

    elif say.find("0X01") >= 0 :

        botsay=weather_survey(say)
    else:
        botsay=say

    return botsay




@app.route("/clock", methods=['GET'])
def clock():

    nowtime = datetime.datetime.now()
    t =  "SELECT * FROM clock"

    cursor.execute(t)
    db.commit()
    # 获取所有记录列表 
    results = cursor.fetchall()

    for row in results: 
        if (row[0]==nowtime.hour) and (row[1]==nowtime.minute):
            return("1")
        else:
            pass
    return("0")

@app.route("/Reminder", methods=['GET'])
def Reminder():

    say=""
    nowtime = datetime.datetime.now()
    week = time.localtime()
    now_week=time.strftime("%w",week)
    now_week=int(now_week)
    if now_week ==0:
        now_week=7

    t =  "SELECT * FROM itinerary"

    cursor.execute(t)
    db.commit()
    # 获取所有记录列表 
    results = cursor.fetchall()

    for row in results: 
        
        #if ((row[0]==nowtime.month) and (row[1]==nowtime.day)) or (row[2]==(nowtime.hour+1)):
        if ((row[0]==nowtime.month) and (row[1]==nowtime.day) and (row[5]==nowtime.year)) or (row[6]==str(now_week) and row[7]==1):
            say+=str(row[2])+"点"+str(row[3])+"分"+row[4]+"\n"

    if(say==""):
        say="0"

    #执行家事
    S ="SELECT * FROM itinerary where year='%d' AND month ='%d' AND day='%d' AND hour ='%d' AND minute ='%d'"% (int(nowtime.year),int(nowtime.month),int(nowtime.day),int(nowtime.hour),int(nowtime.minute))
    cursor.execute(S)
    db.commit()
    results = cursor.fetchall()
    for row in results: 
        if row[4].find("楼") >= 0 :
            C=control_furniture(row[4])
            Add = "UPDATE `furniture_control` SET `number`='%s'"%(str(C))
            cursor.execute(Add)
            db.commit()
        else:
            C=control_all_furniture(row[4])
            Add = "UPDATE `furniture_control` SET `number`='%s'"%(str(C))
            cursor.execute(Add)
            db.commit()
        
    delete ="DELETE FROM itinerary where year<='%d' AND month <='%d' AND day<='%d' AND hour <='%d' AND minute <='%d' AND repeated='%d'"% (int(nowtime.year),int(nowtime.month),int(nowtime.day),int(nowtime.hour),int(nowtime.minute),0)
    cursor.execute(delete)
    db.commit()
    return say


@app.route("/youtube_play", methods=['GET'])
def mov():

    say=song_number()
    return say

@app.route("/wiki", methods=['GET'])
def wiki():
    return search

@app.route("/counter/<string:say>", methods=['GET'])
def count(say):
    """
    global say_time
    say_time=say
    check = s_time()
    if check == "OUT_TIME":
        return "超过时段了"
    else:
        seconds= (int(s_hour) * 3600) + (int(s_minute) * 60) + int(s_second) 
    """
    previous_word=""
    t_minute =0
    t_second =0
    t_hour = 0
    words = jieba.cut(say, cut_all=False)

    for word in words:
        print(word)
        if word =="分钟":

            t_minute=get_int(previous_word)
            t_minute=int(t_minute)

        elif word =="秒":

            t_second=get_int(previous_word)
            t_second=int(t_second)

        elif word =="小时":

            t_hour = get_int(previous_word)
            t_hour=int(t_hour)
            
        previous_word=word

    seconds = t_hour *3600 + t_minute *60 +t_second
    print(seconds)
    return str(seconds) 


@app.route("/check_itinerary", methods=['GET'])
def Check_itinerary():
    check = s_time()
    if check == "OUT_TIME":
        return "超过时段了"
    else:
        pass
    if say_time.find("周")>=0 or say_time.find("星期")>=0 :
        if(s_week ==7):
            if(say_time.find("每")>=0):
                return ("确定是"+"每星期天"+str(s_hour)+"点"+str(s_minute)+"分"+str(event)+"吗")
            else:
                return ("确定是"+str(s_year)+"年"+str(s_month)+"月"+str(s_day)+"日"+"星期天"+str(s_hour)+"点"+str(s_minute)+"分"+str(event)+"吗")
        else:
            if(say_time.find("每")>=0):
                return ("确定是"+"每星期"+str(s_week)+" "+str(s_hour)+"点"+str(s_minute)+"分"+str(event)+"吗")
            else:
                return ("确定是"+str(s_year)+"年"+str(s_month)+"月"+str(s_day)+"日"+"星期"+str(s_week)+" "+str(s_hour)+"点"+str(s_minute)+"分"+str(event)+"吗")
    
    elif say_time.find("每天")>=0:

        return ("确定是"+"每天"+str(s_hour)+"点"+str(s_minute)+"分"+str(event)+"吗")
    else:
        if s_week==7:
            return ("确定是"+str(s_year)+"年"+str(s_month)+"月"+str(s_day)+"日"+"星期天"+str(s_hour)+"点"+str(s_minute)+"分"+str(event)+"吗")
        else:
            return ("确定是"+str(s_year)+"年"+str(s_month)+"月"+str(s_day)+"日"+"星期"+str(s_week)+" "+str(s_hour)+"点"+str(s_minute)+"分"+str(event)+"吗")


def chinese_number(x):
    number = {
        '一':'1',
        '二':'2',
        '三':'3',
        '四':'4',
        '五':'5',
        '六':'6',
        '七':'7',
        '天':'7',
        '日':'7',
        '八':'8',
        '九':'9',
        '十':'10'
    }
    return number.get(x)

def local_city(x):
    local_name = {
        '宜兰':'Yilan_County',
        '花莲':'Hualien_County',
        '台东':'Taitung_County',
        '台南':'Tainan_City',
        '高雄':'Kaohsiung_City',
        '屏东':'Pingtung_County',
        '基隆':'Keelung_City',
        '台北':'Taipei_City',
        '新北':'New_Taipei_City',
        '桃园':'Taoyuan_City',
        '新竹':'Hsinchu_City',
        '苗栗':'Miaoli_County',
        '台中':'Taichung_City',
        '彰化':'Changhua_County',
        '南投':'Nantou_County',
        '云林':'Yunlin_County',
        '嘉义':'Chiayi_County',
        '宜蘭縣':'Yilan_County',
        '花蓮縣':'Hualien_County',
        '台東縣':'Taitung_County',
        '台南市':'Tainan_City',
        '高雄市':'Kaohsiung_City',
        '屏東縣':'Pingtung_County',
        '基隆市':'Keelung_City',
        '臺北市':'Taipei_City',
        '新北市':'New_Taipei_City',
        '桃園市':'Taoyuan_City',
        '新竹縣':'Hsinchu_City',
        '苗栗縣':'Miaoli_County',
        '台中市':'Taichung_City',
        '彰化縣':'Changhua_County',
        '南投縣':'Nantou_County',
        '雲林縣':'Yunlin_County',
        '嘉義市':'Chiayi_County'
    }
    return local_name.get(x,'Taichung_City')
    
def weather(google_weather):

    html =urlopen('http://www.cwb.gov.tw/V7/forecast/taiwan/'+local_city(local)+'.htm').read()

    #html =urlopen('https://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm').read()

    soup = BeautifulSoup(html,'lxml')

    td=soup.find_all('td',limit=12)

    table=['溫度(攝氏):','天气状况:','舒適度:','降雨機率:']
    t=0
    c=[]
    #contents=address+'\n'
    #contents=""
    for i in td:
        if t==1:
            c+=[table[t] + i.img.get('title')]
            t+=1
            continue
        else:
            if t==4:
                t=0
            #contents += table[t] + i.text + '\n'
            if t==0:
                m=i.text.split(' ~ ',1)
                if int(m[0]) <= int(google_weather) <= int(m[1]):
                    c+=[table[t] + google_weather]
                    t+=1
                    continue
            c+=[table[t] + i.text]
            t+=1

    #contents += '天氣狀況：'+soup.find('img')['title']
    nowtime = datetime.datetime.now()
    contents=address
    if (say_time.find("今天晚上")>=0 or say_time.find("今晚")>=0) and int(nowtime.hour)<=18:
        contents += "今晚"+'\n'+c[4]+'\n'+c[5]+'\n'+c[6]+'\n'+c[7]

    elif (say_time.find("今天晚上")>=0 or say_time.find("今晚")>=0) and int(nowtime.hour)>=18:
        contents += "今晚"+'\n'+c[0]+'\n'+c[1]+'\n'+c[2]+'\n'+c[3]

    elif (say_time.find("明天早上")>=0 or say_time.find("明天下午")>=0 or say_time.find("明早")>=0) and int(nowtime.hour)>=18:
        contents += "明早"+'\n'+c[4]+'\n'+c[5]+'\n'+c[6]+'\n'+c[7]


    elif (say_time.find("明天早上")>=0 or say_time.find("明天下午")>=0 or say_time.find("明早")>=0 ) and int(nowtime.hour)<=18:
        contents += "明早"+'\n'+c[8]+'\n'+c[9]+'\n'+c[10]+'\n'+c[11]


    elif (say_time.find("明天晚上")>=0 or say_time.find("明晚")>=0) and int(nowtime.hour)>=18:
        contents += "明晚"+'\n'+c[8]+'\n'+c[9]+'\n'+c[10]+'\n'+c[11]


    elif (say_time.find("明天晚上")>=0 or say_time.find("明晚")>=0) and int(nowtime.hour)<=18:
        contents = "暂无资料"

    elif (say_time.find("明天")>=0 or say_time.find("明天")>=0 ) and int(nowtime.hour)>=18:
        contents += "明早"+'\n'+c[4]+'\n'+c[5]+'\n'+c[6]+'\n'+c[7]


    elif (say_time.find("明天")>=0 or say_time.find("明天")>=0 ) and int(nowtime.hour)<=18:
        contents += "明早"+'\n'+c[8]+'\n'+c[9]+'\n'+c[10]+'\n'+c[11]

    elif (say_time.find("今天早上")>=0 or say_time.find("早上")>=0 or say_time.find("下午")>=0 or say_time.find("今天下午")>=0 or say_time.find("今早")>=0) and int(nowtime.hour)>=18:
        contents ="超过时段了"
    else:
        contents += "现在"+'\n'+c[0]+'\n'+c[1]+'\n'+c[2]+"\n"+c[3]


    return contents


def song_number():

    sg=quote(song,'utf-8')

    html =urlopen('https://www.youtube.com/results?search_query='+sg).read()

    soup = BeautifulSoup(html,'lxml')

    a=soup.find('a'," yt-uix-sessionlink spf-link ")

    s=a['href']

    return s


def date(s,oth=''):
    s2=s.lower()
    s1="0123456789月日点分" 
    for c in s2:
        if c not in s1:
            s=s.replace(c,'')
    return s

def get_int(s,oth=''):
    """
    s2=s.lower()
    s1="0123456789" 
    m=""
    for c in s2:
        if c  in s1:
            m+=c
    return m
    """
    s2=s.lower()
    s1="十九八七六五四三二一" 
    s3="0123456789"
    m=""
    for c in s2:
        if c  in s1:
            c = chinese_number(c)
            m+=c
        elif c in s3:
            m+=c

    if m=="":
        return "0"
    else:
        return m

def get_week(s,oth=''):
    s2=s.lower()
    s1="一二三四五六天日" 
    m=""
    for c in s2:
        if c  in s1:
            m+=c
        else:
            break
    return m

def s_time():

    global s_year,s_month,s_day,s_hour,s_minute,s_second,s_week
    nowtime = datetime.datetime.now()

    s_year=int(nowtime.year)

    if say_time.find("月") >= 0:
        s="月"
        s_month=say_time[say_time.find(s)-2:say_time.find(s)]           
        if s_month =="":
            s_month=say_time[say_time.find(s)-1:say_time.find(s)]
        s_month=get_int(s_month)
    else:
        s_month=nowtime.month
    
    if  say_time.find("日") >=0:
        s1='日'
        s_day=say_time[say_time.find(s1)-2:say_time.find(s1)]
        if s_day =="":
            s_day=say_time[say_time.find(s1)-1:say_time.find(s1)]
        s_day=get_int(s_day)
    else:
        s_day=int(nowtime.day)
        if say_time.find("明天") >=0:
            s_day+=1

        if say_time.find("后天") >=0:
            s_day+=2
    
    if say_time.find("点") >= 0 or say_time.find("小时") >= 0:
        
        if say_time.find("点") >= 0:
            s2="点"
            s_hour=say_time[say_time.find(s2)-2:say_time.find(s2)]
            if s_hour=="":
                s_hour=say_time[say_time.find(s2)-1:say_time.find(s2)]
            s_hour=get_int(s_hour) 

        if say_time.find("小时") >= 0:
            s2="小"
            s_hour=say_time[say_time.find(s2)-2:say_time.find(s2)]
            if s_hour=="":
                s_hour=say_time[say_time.find(s2)-1:say_time.find(s2)]
            s_hour=get_int(s_hour) 
    else:
        s_hour="0"


    if say_time.find("分") >=0:
        s3="分"
        s_minute=say_time[say_time.find(s3)-2:say_time.find(s3)]
        if s_minute =="":
            s_minute=say_time[say_time.find(s3)-1:say_time.find(s3)]
        s_minute=get_int(s_minute)
    else:
        s_minute="0"

    if say_time.find("秒") >=0:
        s3="秒"
        s_second=say_time[say_time.find(s3)-2:say_time.find(s3)]
        if s_second =="":
            s_second=say_time[say_time.find(s3)-1:say_time.find(s3)]
        s_second=get_int(s_second)
    else:
        s_second="0"

    if say_time.find("星期") >=0:
        s4="星期"
        s_week=say_time[say_time.find(s4)+2:say_time.find(s4)+3]
        s_week=chinese_number(s_week)
        s_week=int(s_week)
    elif say_time.find("周")>=0:
        s4="周"
        s_week=say_time[say_time.find(s4)+1:say_time.find(s4)+2]
        s_week=chinese_number(s_week)
        s_week=int(s_week) 
    else:
        s_year=int(nowtime.year)
        if say_time.find("明年") >=0 or int(s_month) < int(nowtime.month) or (int(s_month)==int(nowtime.month) and int(s_day) < int(nowtime.day)):
            s_year+=1

        if say_time.find("后年") >=0:
            s_year+=2
        d=str(s_year)+str(s_month)+str(s_day)
        a=datetime.datetime.strptime(d,"%Y%m%d").weekday()+1 
        s_week=str(a)
        s_week=int(s_week)


    s_month=int(s_month)
    s_day=int(s_day)
    s_hour=int(s_hour)
    s_minute=int(s_minute)
    s_week=int(s_week)



    if say_time.find("晚上") >=0 or say_time.find("下午") >=0 :
        s_hour+=12

    if say_time.find("点半") >=0:
        s_minute+=30

    if(say_time.find("星期")>=0) or (say_time.find("周")>=0):
        if(say_time.find("下星期")>=0) or (say_time.find("下周")>=0):
            week = time.localtime()
            now_week=time.strftime("%w",week)
            now_week=int(now_week)
            s=say_time

            if now_week ==0:
                now_week =7
            s1="下星期周" 
            for c in s:
                if c not in s1:
                    s=s.replace(c,'')

            #s2=s.lower()
            s1="下" 
            m=""
            for c in s:
                if c  in s1:
                    m+=c
                else:
                    break
            s=time.time()
            s=int(s)
            s+=604800*m.count("下")
            if(now_week > s_week):
                s-=86400*(now_week-s_week)
            else:
                s+=86400*(s_week-now_week)
            timeArray=time.localtime(s)
            s_year=int(time.strftime("%Y",timeArray))
            s_month=int(time.strftime("%m",timeArray))
            s_day=int(time.strftime("%d",timeArray))

        else:
            if say_time.find("每") >= 0:
                pass
            else:
                week = time.localtime()
                now_week=time.strftime("%w",week)
                now_week=int(now_week)
                s=say_time

                if now_week ==0:
                    now_week =7

                s=time.time()
                s=int(s)
                if(now_week > s_week):
                    pass
                else:
                    s+=86400*(s_week-now_week)
                timeArray=time.localtime(s)
                s_year=int(time.strftime("%Y",timeArray))
                s_month=int(time.strftime("%m",timeArray))
                s_day=int(time.strftime("%d",timeArray))

    print(s_year,s_month,s_day,s_hour,s_minute,s_week)
    if say_time.find("每") >= 0:
            return "OK"
    elif (s_month == nowtime.month) and (s_day == nowtime.day):

        if (s_hour < nowtime.hour) or ((s_hour == nowtime.hour) and (s_minute < nowtime.minute)):
            return "OUT_TIME"

        else:
            return "OK"

    else:
        return "OK"
@app.route("/itinerary", methods=['GET'])
def itinerary():
    global say_time
    if  say_time.find("年") >= 0 or say_time.find("月") >= 0 or say_time.find("日") >= 0 or say_time.find("今天") >= 0 or say_time.find("明天") >= 0 or say_time.find("后天") >= 0 or say_time.find("星期") >= 0 or say_time.find("点") >= 0 or say_time.find("礼拜") >= 0:
        check = s_time()
        if say_time.find("今天") >= 0 :
            pass
        elif check == "OUT_TIME":
            return "超过时段了"
        else:
            pass
        content =  "SELECT * FROM itinerary \
        WHERE year='%d' AND month ='%d' AND day='%d' OR (week='%s' AND repeated='%d')"%(s_year,s_month,s_day,s_week,1)

        cursor.execute(content)
        db.commit()
        # 获取所有记录列表 
        results = cursor.fetchall()
        say=""

        for row in results: 

            if row[7] == 1  :
                say+="惯例每周"+str(s_week)+" "+str(row[2])+"点"+str(row[3])+"分"+row[4]+"\n"
            
            else:               
                say+=str(row[2])+"点"+str(row[3])+"分"+row[4]+"\n"

    else:
        content =  "SELECT * FROM itinerary \
        WHERE event='%s'"%(event)
        cursor.execute(content)
        db.commit()
        # 获取所有记录列表 
        results = cursor.fetchall()
        say=""
        c=0

        for row in results: 

            if row[7] == 1 :
                c +=1
            else:
                say+=str(row[0])+"月"+str(row[1])+"日"+str(row[2])+"点"+str(row[3])+"分"+row[4]+"\n"

        if c==7:
            say+="惯例每天"+" "+str(row[2])+"点"+str(row[3])+"分"+row[4]+"\n"
        else:

            for row in results: 

                if row[7] == 1 :
                    say+="惯例每周"+str(row[6])+" "+str(row[2])+"点"+str(row[3])+"分"+row[4]+"\n"
                

    if say=="":
        return ("查无行程")   
    else:
        return say
"""
@app.route("/itinerary", methods=['GET'])
def deitinerary():
    check = s_time()


    if say_time.find("每天")>=0:
        #content =  "SELECT * FROM itinerary \
        #WHERE hour='%d' AND minute='%d'"%(s_hour,s_minute)
        return "确定是每天"+str(s_hour)+"点"+str(s_minute)+"分吗"
    elif say_time.find("点")>=0:
        content =  "SELECT * FROM itinerary \
        WHERE (year='%d' AND month ='%d' AND day='%d' AND hour='%d' AND minute='%d') OR (hour='%d' AND minute='%d' AND week='%s' AND repeated='%d')"%(s_year,s_month,s_day,s_hour,s_minute,s_hour,s_minute,s_week,1)
    else:
        content =  "SELECT * FROM itinerary \
        WHERE (year='%d' AND month ='%d' AND day='%d')"%(s_year,s_month,s_day)

    cursor.execute(content)
    db.commit()
    # 获取所有记录列表 
    results = cursor.fetchall()
    say=""

    for row in results: 

        if row[7] == 1 :
            say+="惯例每周"+str(s_week)+" "+str(row[2])+"点"+str(row[3])+"分"+row[4]+"\n"
           
        else:               
            say+=str(row[2])+"点"+str(row[3])+"分"+row[4]+"\n"

    

    if say=="":
        return ("0")   
    else:
        return "确定是"+say+"吗"
"""


def Add_itinerary():  

    check = s_time()
    if check == "OUT_TIME":
        return "超过时段了"
    else:
        pass

    if (say_time.find("星期")>=0) or (say_time.find("周")>=0):
        if say_time.find("每星期")>=0 or say_time.find("每周")>=0:
            Add = "INSERT INTO itinerary(year,month,day,week,hour,minute,event,repeated) \
            VALUES ('%d','%d','%d','%s','%d','%d','%s','%d')"%(0,0,0,s_week,s_hour,s_minute,event,1)
            cursor.execute(Add)
            db.commit() #存進sql
        else:   
            Add = "INSERT INTO itinerary(year,month,day,week,hour,minute,event,repeated) \
            VALUES ('%d','%d','%d','%s','%d','%d','%s','%d')"%(s_year,s_month,s_day,s_week,s_hour,s_minute,event,0)
            cursor.execute(Add)
            db.commit() #存進sql

    elif say_time.find("每天")>=0: 

        for week in range(1,8):
            Add = "INSERT INTO itinerary(year,month,day,week,hour,minute,event,repeated) \
            VALUES ('%d','%d','%d','%d','%d','%d','%s','%d')" % (0,0,0,week,s_hour,s_minute,event,1)
            cursor.execute(Add)
            db.commit() #存進sql
    else:

        Add = "INSERT INTO itinerary(year,month,day,week,hour,minute,event,repeated) \
        VALUES ('%d','%d','%d','%d','%d','%d','%s','%d')" % (s_year,s_month,s_day,s_week,s_hour,s_minute,event,0)
        cursor.execute(Add)
        db.commit() #存進sql

def Delete_itinerary():
    """
    check = s_time()
    if check == "OUT_TIME":
        return "超过时段了"
    else:
        pass
    """
    if say_time.find("星期")>=0 or say_time.find("周")>=0:
        if say_time.find("每星期")>=0 or say_time.find("每周")>=0:
            Add = "DELETE FROM itinerary WHERE week='%d' AND hour='%d' AND minute='%d'"%(s_week,s_hour,s_minute)
            cursor.execute(Add)
            db.commit() #存進sql
        else:   
            Add = "DELETE FROM itinerary WHERE year='%d' AND month='%d' AND day='%d' \
            AND week='%d' AND hour='%d' AND minute='%d' AND repeated='%d'" % (s_year,s_month,s_day,s_week,s_hour,s_minute,0)
            cursor.execute(Add)
            db.commit() #存進sql

    elif say_time.find("每天")>=0: 

            Add = "DELETE FROM itinerary WHERE\
            hour='%d' AND minute='%d' " % (s_hour,s_minute)
            cursor.execute(Add)
            db.commit() #存進sql

    elif say_time.find("点")>=0: 
        Add = "DELETE FROM itinerary WHERE year='%d' AND month='%d' AND day='%d' \
        AND week='%d' AND hour='%d' AND minute='%d' AND repeated='%d'" % (s_year,s_month,s_day,s_week,s_hour,s_minute,0)
        cursor.execute(Add)
        db.commit() #存進sql

    elif say_time.find("月")>=0: 
        Add = "DELETE FROM itinerary WHERE  month='%d' AND day='%d'" % (s_month,s_day)
        cursor.execute(Add)
        db.commit() #存進sql
    else:
        """
        d=str(s_year)+str(s_month)+str(s_day)
        a=datetime.datetime.strptime(d,"%Y%m%d").weekday()+1 
        Add = "DELETE FROM itinerary WHERE (year='%d' AND month='%d' AND day='%d' AND week='%s' AND hour='%d' AND minute='%d') \
        OR (hour='%d' AND minute='%d' AND week='%s' AND repeated='%d')"%(s_year,s_month,s_day,s_week,s_hour,s_minute,s_hour,s_minute,s_week,1)
        cursor.execute(Add)
        db.commit() #存進sql
        """
        Add = "DELETE FROM itinerary WHERE event ='%s'" % (event)
        cursor.execute(Add)
        db.commit() #存進sql

def conflict():
    check = s_time()
    if check == "OUT_TIME":
        return "2"
    else:
        pass
    w_hour=s_hour-1
    l_hour=s_hour+1
    """
    w_minute=s_minute+30
    w_hour=s_hour

    if w_minute >=60:
        w_hour+=1
        w_minute-=60

    l_minute=s_minute-30
    l_hour=s_hour
    if l_minute<0:
        l_hour-=1
        l_minute+=60

    
    jug="SELECT * FROM itinerary \
        WHERE ((month ='%d' AND day ='%d' AND year='%d') OR (week='%d' AND repeated='1'))\
        AND (((hour ='%d') AND (minute BETWEEN 0 AND 30))\
        OR ((hour = '%d') AND (minute BETWEEN 30 AND 59)))"%(s_month,s_day,s_year,s_week,w_hour,l_hour)
    """
    jug="SELECT * FROM itinerary \
    WHERE ((month ='%d' AND day ='%d' AND year='%d') OR (week='%d' AND repeated='1'))\
    AND ((hour ='%d')or (hour ='%d'))"%(s_month,s_day,s_year,s_week,w_hour,l_hour)


    cursor.execute(jug)
    db.commit()
    results = cursor.fetchall()
    x=0
    for row in results:
        x+=1
    if x>0:
        return ("1")
    else:
        return ("0")
    
def Ad_clock():

    nowtime = datetime.datetime.now()


    if say_time.find("分钟后") >=0 :
        add = get_int(say_time)
        add = int(add)

        s_minute = nowtime.minute
        s_hour= nowtime.hour

        s_hour=int(s_hour)
        s_minute=int(s_minute)
        s_minute += add
        Add = "INSERT INTO clock(hour,minute) \
        VALUES ('%d','%d')" % (s_hour,s_minute)

    elif say_time.find("小时后") >=0 :
        add = get_int(say_time)
        add = int(add)
        
        s_minute = nowtime.minute
        s_hour= nowtime.hour

        s_hour=int(s_hour)
        s_minute=int(s_minute)
        s_hour += add
        Add = "INSERT INTO clock(hour,minute) \
        VALUES ('%d','%d')" % (s_hour,s_minute)

    else:
        if say_time.find("点")>=0:
            s="点"
            s_hour=say_time[say_time.find(s)-2:say_time.find(s)]
            if s_hour=="":
                s_hour=say_time[say_time.find(s)-1:say_time.find(s)]
            s_hour=get_int(s_hour)
        else:
            s_hour=nowtime.hour

        if say_time.find("分")>=0:
            s3="分"
            s_minute=say_time[say_time.find(s3)-2:say_time.find(s3)]
            if s_minute=="":
                s_minute=say_time[say_time.find(s3)-1:say_time.find(s3)]
            s_minute=get_int(s_minute)
        else:
            s_minute="0"

        s_hour=int(s_hour)
        s_minute=int(s_minute)

        if (say_time.find("下午") >= 0) or (say_time.find("晚上") >= 0):
            s_hour+=12
        Add = "INSERT INTO clock(hour,minute) \
        VALUES ('%d','%d')" % (s_hour,s_minute)

    cursor.execute(Add)
    db.commit() #存進sql

def segmented(iterable):
    def _seg(width):
        it = iterable
        while len(it) > width:
            yield it[:width]
            it = it[width:]
        yield it

    return _seg

def control_furniture(say):

    if say.find("一楼") >= 0 or say.find("1楼") >= 0 :
        s=say.lower()
        s1="开"
        s2="1一"
        s3="2二"
        s4="关"
        m=""
        op=0
        f=0

        for c in s:
            if (c in s4):
                op=0
            if (c in s3):
                f=0
            if (c  in s1) :
                m += c
                op=1
            if  ((c in s2 ) or f==1) and op==1 :
                f=1
                m+=c

        if m.find("全部") >= 0 :
            light_number1[0] = '1'
            light_number1[1] = '1'
            light_number1[2] = '1'
            light_number1[3] = '1'

        if m.find("客厅") >= 0 :
            light_number1[0] = '1'

        if m.find("厨房") >= 0 :
            light_number1[1] = '1'

        if m.find("阳台") >= 0 :
            light_number1[2] = '1'

        if m.find("楼梯") >= 0 :
            light_number1[3] = '1'

        s=say.lower()
        s1="关"
        s2="1一"
        s3="2二"
        s4="开"
        m=""
        op=0
        f=0

        for c in s:

            if (c in s4):
                op=0

            if (c in s3):
                f=0
            if (c  in s1) :
                m += c
                op=1
            if  ((c in s2 ) or f==1) and op==1 :
                f=1
                m+=c

        if m.find("全部") >= 0 :
            light_number1[0] = '0'
            light_number1[1] = '0'
            light_number1[2] = '0'
            light_number1[3] = '0'

        if m.find("客厅") >= 0 :
            light_number1[0] = '0'

        if m.find("厨房") >= 0 :
            light_number1[1] = '0'

        if m.find("阳台") >= 0 :
            light_number1[2] = '0'

        if m.find("楼梯") >= 0 :
            light_number1[3] = '0'


    if say.find("二楼") >= 0 or say.find("1楼") >= 0:

        s=say.lower()
        s1="开"
        s2="2二"
        s3="1一"
        s4="关"
        m=""
        op=0
        f=0

        for c in s:
            if( c in s4):
                op=0
            if (c in s3):
                f=0
            if (c  in s1) :
                m += c
                op=1
            if  ((c in s2 ) or f==1) and op==1 :
                f=1
                m+=c

        if m.find("全部") >= 0 :
            light_number1[6] = '1'
            light_number1[7] = '1'
            light_number1[8] = '1'

        if m.find("房间") >= 0 :
            light_number1[6] = '1'

        if m.find("楼梯") >= 0 :
            light_number1[7] = '1'

        if m.find("阳台") >= 0 :
            light_number1[8] = '1'

        s=say.lower()
        s1="关"
        s2="2二"
        s3="1一"
        s4="开"
        m=""
        op=0
        f=0

        for c in s:

            if (c in s4):
                op=0

            if (c in s3):
                f=0
            if (c  in s1) :
                m += c
                op=1
            if  ((c in s2 ) or f==1) and op==1 :
                f=1
                m+=c

        if m.find("全部") >= 0 :
            light_number1[6] = '0'
            light_number1[7] = '0'
            light_number1[8] = '0'

        if m.find("房间") >= 0 :
            light_number1[6] = '0'

        if m.find("楼梯") >= 0 :
            light_number1[7] = '0'

        if m.find("阳台") >= 0 :
            light_number1[8] = '0'

    #阵列转字串
    light ="".join(light_number1)

    return light

def control_all_furniture(say):

    if say.find("开")>= 0:

        if say.find("全部") >= 0 :
            light_number1[0] = '1'
            light_number1[1] = '1'
            light_number1[2] = '1'
            light_number1[3] = '1'
            light_number1[6] = '1'
            light_number1[7] = '1'
            light_number1[8] = '1'

        if say.find("客厅") >= 0 :
            light_number1[0] = '1'

        if say.find("厨房") >= 0 :
            light_number1[1] = '1'

        if say.find("阳台") >= 0 :
            light_number1[2] = '1'
            light_number1[8] = '1'

        if say.find("楼梯") >= 0 :
            light_number1[3] = '1'
            light_number1[7] = '1'

        if say.find("房间") >= 0 :
            light_number1[6] = '1'
    
    if say.find("关")>= 0:

        if say.find("全部") >= 0 :
            light_number1[0] = '0'
            light_number1[1] = '0'
            light_number1[2] = '0'
            light_number1[3] = '0'
            light_number1[6] = '0'
            light_number1[7] = '0'
            light_number1[8] = '0'

        if say.find("客厅") >= 0 :
            light_number1[0] = '0'

        if say.find("厨房") >= 0 :
            light_number1[1] = '0'

        if say.find("阳台") >= 0 :
            light_number1[2] = '0'
            light_number1[8] = '0'

        if say.find("楼梯") >= 0 :
            light_number1[3] = '0'
            light_number1[7] = '0'

        if say.find("房间") >= 0 :
            light_number1[6] = '0'

    light ="".join(light_number1)

    return light

def weather_survey(say):
    local=["宜兰","花莲","台东","台南","高雄","屏东","基隆","台北","新北","桃园","新竹","苗栗","台中","彰化","南投","云林","嘉义"]
    rain_small=20
    rain_large=30
    rain_small_local=""
    rain_large_local=""
    for i in local:

        html =urlopen('http://www.cwb.gov.tw/V7/forecast/taiwan/'+local_city(i)+'.htm').read()


        soup = BeautifulSoup(html,'lxml')

        td=soup.find_all('td',limit=12)
        t=1
        miss="% "
        rain=""
        for j in td:
            if t !=4:
                t+=1
                continue
            else:
                for k in j.text:
                    if k in miss:
                        k=""
                    else:
                        rain+=k  
                break
        if int(rain) <= rain_small:
            rain_small_local+=i
        if int(rain) >= rain_large:
            rain_large_local+=i  
    if len(rain_large_local) <= 8:
        if len(rain_large_local) == 0:
            return ("全台天气都很好")
        else:
            return ("大部分天气都很好就只有"+rain_large_local+"会下雨")
    elif len(rain_small_local) <= 8:
        if len(rain_small_local) == 0:
            return("全台天气都不好")
        else:
            return("大部分天气都不好就只有"+rain_small_local+"会晴天")
    elif say.find("下雨") >0 :
        return(rain_large_local+"会下雨")
    elif say.find("晴天") >0 :
        return(rain_small_local+"会晴天")

def weather_air(say):

    html =requests.get('http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=xml')
    soup = BeautifulSoup(html.text,"html.parser")

    city_tag = soup.find_all('county')
    air_tag  = soup.find_all('status')
    PM_tag = soup.find_all('pm2.5_avg')
    PM_large=0

    s2=say.lower()
    s1="宜兰花莲台东台南高雄屏东基隆台北新北桃园新竹苗栗台中彰化南投云林嘉义宜蘭花蓮台東台南高雄屏東基隆台北新北桃園新竹苗栗臺中彰化南投雲林嘉義"
    m=""
    for c in s2:
        if c  in s1:
            m+=c

    local=traditional_to_Simplified(m)

    for i,j,k in zip(city_tag,air_tag,PM_tag):
        if i.text == local :
            try:
                if int(k.text) >= PM_large:
                    PM_large=int(k.text)
                    city=i.text
                    air=j.text
                    PM=k.text
            except:
                continue

    if int(PM)>=30:
        air +="\n"+"外出记得戴口罩唷"
    return(city+"的PM2.5最高是:"+PM+"\n"+"空气品质:"+air)
    #return(city+"的空气品质:"+air)

def traditional_to_Simplified(x):
    local_name = {
        '宜兰':'宜蘭縣',
        '花莲':'花蓮縣',
        '台东':'臺東',
        '台南':'臺南市',
        '高雄':'高雄市',
        '屏东':'屏東縣',
        '基隆':'基隆市',
        '台北':'臺北市',
        '新北':'新北市',
        '桃园':'桃園市',
        '新竹':'新竹縣',
        '苗栗':'苗栗縣',
        '台中':'臺中市',
        '彰化':'彰化縣',
        '南投':'南投縣',
        '云林':'雲林縣',
        '嘉义':'嘉義縣',
        '宜蘭':'宜蘭縣',
        '花蓮':'花蓮縣',
        '台東':'臺東',
        '臺東':'臺東',
        '臺南':'臺南市',
        '屏東':'屏東縣',
        '桃園':'桃園市',
        '雲林':'雲林縣',
        '嘉義':'嘉義縣'
    }
    return local_name.get(x,'臺中市')  

def station_number(TrainStation):

    with open('./Documents/primary/Train/TrainStation_Number.json', 'r',encoding='utf-8') as f:
        data3 = json.load(f)

    return(data3[0][TrainStation])

def train(hour,minute,time):

    a = Auth(app_id, app_key)
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/OD/'+Departure_station+'/to/'+Destination_station+'/'+time+'?$top=30&format=json', headers= a.get_auth_header())
    #print(response.content.decode('utf-8'))
    trainObject = response.content.decode('utf-8')
    jsonString = json.loads(trainObject)
    ticket=""
    for i in range(0,100,1):
        try:
            train_number = jsonString[i]['DailyTrainInfo']['TrainNo']
            train_name = jsonString[i]['DailyTrainInfo']['TrainTypeName']['Zh_tw']
            DepartureTime = jsonString[i]['OriginStopTime']['DepartureTime']
            T=DepartureTime.split(':',1)
            if (hour == int(T[0])) or (hour ==int(T[0]) and minute < int(T[1])):
                ArrivalTime = jsonString[i]['DestinationStopTime']['ArrivalTime']
                print("車次:  " +train_number)
                print("車種:  "+train_name)
                print("出發點:  "+DepartureTime)
                print("到站時間點:  "+ArrivalTime)
                print("------------------------")
                ticket +="車次:"+train_number +'\n'+train_name+'\n'+"出發點:  "+DepartureTime+'\n'+"到站時間點:  "+ArrivalTime+'\n\n'
        except IndexError:
            break

    return ticket


if __name__ == '__main__':
    a=webbrowser.get('google-chrome')
    a.open("http://localhost/test.html")
    app.run(host='0.0.0.0', debug=False)

   

   

