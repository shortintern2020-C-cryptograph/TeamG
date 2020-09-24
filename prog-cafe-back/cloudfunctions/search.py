from flask import jsonify
import redis
import json

# @author Tanaka Koki

url="redis://h:p67a72fdc9e0b5ff64d97388a2890aad0f232e1345a94014540b23bcdd14f4242@ec2-50-16-12-122.compute-1.amazonaws.com:15169"
r = redis.from_url(url)

def search(request):
    #requestパラメータの取得
    query=request.args.get('q') 
    u_id=request.args.get('userId') 

    #DBから一致id取得
    idlist= r.keys('user:'+query+'*')[:30]
    #infoを取得しながらjson整形
    ret_str='{'
    n=len(idlist)
    if(n!=0):
        for id_ in idlist:
            info_dic=r.hgetall(id_)
            #check follow
            decodec_id=id_[5:].decode()
            following_list = r.zrange('following:'+u_id,0,-1)
            following_list = [str(f.decode()) for f in following_list]
            n=n-1
            if(not(str(decodec_id) == str(u_id))):
                ret_str+='\"'+id_[5:].decode()+'\"'+':{'
                ret_str+='\"name\":\"'
                ret_str+=str(info_dic[b'name'].decode())
                ret_str+='\",'
                ret_str+='\"rank\":\"'
                try:
                    if(info_dic[b'rank']!=None):
                        ret_str+=str(info_dic[b'rank'].decode())
                    else:
                        ret_str+="砂"
                except:
                    ret_str+="砂"
                ret_str+='\",'
                ret_str+='\"skills\":[\"'
                ret_str+=str(info_dic[b'skills'].decode().replace(",","\",\""))
                ret_str+='\"],'
                ret_str+='\"login_time\":\"'
                ret_str+=str(info_dic[b'login_time'].decode())
                ret_str+='\",'
                ret_str+='\"online\":'
                ret_str+=str(info_dic[b'online'].decode())
                ret_str+=','
                ret_str+='\"following\":'
                print()
                print(decodec_id)
                print(following_list)
                print()
                if(decodec_id in following_list):
                    ret_str+='true'
                else:
                    ret_str+='false'
                ret_str+='}'

                if(n is not 0):
                    ret_str+=','
        ret_str+='}'
        print(ret_str)
    else:
        ret_str='{}'
    response=jsonify(json.loads(ret_str))
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    return  response




