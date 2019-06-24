import time
import datetime

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
def s_time(say_time):

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

    print(s_year,"年/ ",s_month,'月/ ',s_day,'日/ ',s_hour,'点/ ',s_minute,'分/ ','星期',s_week)
    if say_time.find("每") >= 0:
            return "OK"
    elif (s_month == nowtime.month) and (s_day == nowtime.day):

        if (s_hour < nowtime.hour) or ((s_hour == nowtime.hour) and (s_minute < nowtime.minute)):
            return "OUT_TIME"

        else:
            return "OK"

    else:
        return "OK"


s_time("明天下午5点10分上课")