from flask import Flask, request,jsonify
import redis
import json

# @author Suzuki Hijiri


#dbに接続
url="redis://h:p67a72fdc9e0b5ff64d97388a2890aad0f232e1345a94014540b23bcdd14f4242@ec2-50-16-12-122.compute-1.amazonaws.com:15169"
r = redis.from_url(url)
bs='\"' # " 


def user(request):
	userid=json.loads((request.data.decode()))["id"]
	to=json.loads((request.data.decode()))["to"]
	show_follow=json.loads((request.data.decode()))["show_follow"]

	
	user=r.hgetall("user:"+to)
	myfollowing_list = r.zrange('following:'+userid,0,-1)
	myfollowing_list = [f.decode() for f in myfollowing_list]
	
	following_list = r.zrange('following:'+to,0,-1)
	following_list = [f.decode() for f in following_list]
	jsonstr='{'
	for i in user:
		if(i.decode()=="skills"):
			jsonstr+=bs+i.decode()+bs+':'
			jsonstr+='[\"'+r.hget("user:"+to,i.decode()).decode().replace("\'","").replace(",","\",\"")+'\"]'
			jsonstr+=','
		elif(i.decode()=="online"):
			jsonstr+=bs+i.decode()+bs+':'
			jsonstr+=r.hget("user:"+to,i.decode()).decode()
			jsonstr+=','
		else:
			jsonstr+=bs+i.decode()+bs+':'
			jsonstr+=bs+r.hget("user:"+to,i.decode()).decode()+bs
			jsonstr+=','			
		
	
	jsonstr+=bs+"following"+bs+':'
	if(to in myfollowing_list):
		jsonstr+="true"
	else:
		jsonstr+="false"
	
	if(show_follow==True):
		following_list=str(following_list).replace("'",'"')
		print(following_list)
		jsonstr+=','
		jsonstr+=bs+'following_list'+bs+':'
		jsonstr+=following_list
	jsonstr+='}'
	response=jsonify(json.loads(jsonstr))
	response.headers.set('Access-Control-Allow-Origin', '*')
	response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
	return  response