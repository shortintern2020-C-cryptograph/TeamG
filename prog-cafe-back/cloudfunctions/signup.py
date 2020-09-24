from flask import Flask, request,jsonify
import redis
import json
import requests
import time
import re
from bs4 import BeautifulSoup
from ast import literal_eval

# @author Tanaka Koki

loadurl1="https://github-readme-stats.vercel.app/api/top-langs/?username="
loadurl2="&layout=compact"

url="redis://h:p67a72fdc9e0b5ff64d97388a2890aad0f232e1345a94014540b23bcdd14f4242@ec2-50-16-12-122.compute-1.amazonaws.com:15169"
r = redis.from_url(url)


class Param():
    id: str



def signup(request):
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
            }
        return ('', 204, headers)


    param=Param()
    print()
    param.id=json.loads(str(request.data.decode()))["id"]
    #githubから情報取得
    user_dict=json.loads(requests.get("https://api.github.com/users/"+param.id).text)
    if(r.hget("user:"+str(param.id),"rank")==None):
        #新規
        print("signup")
        html = requests.get(loadurl1+param.id+loadurl2).text
        soup = BeautifulSoup(html, "html.parser")
        skills_html=soup.select('.lang-name')
        skills="{"
        i=len(skills_html)
        for skill in skills_html:
            skills+=skills+"\""+re.sub("\\d","",str(skill.string).replace(" ","")[1:-6])+"\""
            i=i+1
            if(not(i==len(skills_html)-1)):
                skills+=","
        print(skills)
        skills=set(literal_eval(skills.replace("{","").replace("}","").replace("\"\"","\",\"")))  
        print("2:",str(skills))
        print("username:",param.id) 
        print("userdict:",user_dict)
        print("skills:",skills)
        print(str(int(time.time())))
        r.hmset("user:"+str(param.id),  {"name":str(user_dict['name']),"rank":'砂',"skills":str(skills)[1:-1],"sum_login_time":0,"login_time":int(time.time()),"online":"true"})

        r.set("online:"+param.id,time.time())
    else:
        #既存
        print("login")
        print("userinfo below")
        print(str(r.hgetall("user:"+str(param.id))))
        print("userinfo above")

        html = requests.get(loadurl1+param.id+loadurl2).text
        soup = BeautifulSoup(html, "html.parser")
        skills_html=soup.select('.lang-name')
        skills="{"
        i=len(skills_html)
        for skill in skills_html:
            skills+=skills+"\""+re.sub("\\d","",str(skill.string).replace(" ","")[1:-6])+"\""
            i=i+1
            if(not(i==len(skills_html)-1)):
                skills+=","
        print(skills)
        skills=set(literal_eval(skills.replace("{","").replace("}","").replace("\"\"","\",\"")))  
        print("2:",str(skills))
        print("username:",param.id) 
        print("userdict:",user_dict)
        print("skills:",skills)
        print(str(int(time.time())))
        r.hmset("user:"+str(param.id),  {"name":str(user_dict['name']),"skills":str(skills)[1:-1],"login_time":int(time.time()),"online":"true"})        #sum_logintime以外変更
        #r.hmset("user:"+param.id,  {"name":user_dict['name'],"skills":str(skills),"login_time":int(time.time()),"online":"true"})
        r.set("online:"+param.id,time.time())    #room配分
    #空いているルームを取得
    i=0
    room_num=len(r.keys("room:*"))
    roomid=0
    
    for i in range(room_num+1):
        
        # @auther Suzuki Hiijiri fix################
        
        num=len(r.hgetall("room:"+str(i)))#ルームの人数
        if( ( num <8) and (param.id.encode() not in r.hgetall("room:"+str(i)).values()) ):
            print("exist room→"+str(i))
            #入室
            room_member=[f.decode() for f in r.hkeys("room:"+str(i))]
            print("roommember",room_member)
            print("num+1",str(num+1))
            for u_num in range(num+1):
                print("u_num")

                if(str(u_num) not in room_member):
                    print("not in")
                    r.hmset("room:"+str(i),{ u_num :  param.id})
                    break
        #################################
        
            roomid=i
            break
        elif(i==room_num-1):
            #新規ルーム作成
            print("new room→"+str(i+1))
            r.hmset("room:"+str(i+1),{0  :  param.id})
            roomid=i+1
            break
        if(i==room_num):
            break
    r.hmset("user:"+param.id,  {"roomid":roomid})
    users=str(list(r.hgetall("room:"+str(roomid)).values())).replace("b","").replace("\'","\"")
    ret_str="{\"id\":"+str(roomid)+",\"users\":"+users+" }"
    print("response::",json.loads(ret_str))
    response=jsonify(json.loads(ret_str))
    response.headers.set('Content-Type', 'application/json')
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type')

    return  response

