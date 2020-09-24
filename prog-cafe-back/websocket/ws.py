from fastapi import FastAPI,WebSocketDisconnect
from starlette.websockets import WebSocket
import uvicorn
import redis
import json
import time
from fastapi.middleware.cors import CORSMiddleware
#import leave
import random



"""
入室
状態
切断
個チャ
"""

 #@author Tanaka Koki, Suzuki Hijiri

app = FastAPI()


# 辞書
#class Users:
#    def __init__(self):
#        self.ClientId2Key = {}
#        self.ClientKey2Id = {}
#        self.ClientKey2Ws = {}
#    def set(self,ID,KEY,WS):
#        self.ClientKey2Ws.update({KEY: WS})
#        self.ClientId2Key.update({ID:KEY})
#        self.ClientKey2Id.update({KEY: ID})

rooms={}

        
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


url="redis://h:p67a72fdc9e0b5ff64d97388a2890aad0f232e1345a94014540b23bcdd14f4242@ec2-50-16-12-122.compute-1.amazonaws.com:15169"
r = redis.from_url(url)

#仮のユーザーID
userid="nishimura"

#仮のキー
keys=[]




@app.get('/') # methodとendpointの指定
async def hello():
    return {"text": "hello world!"}

#@app.get('/clear') # methodとendpointの指定
#async def hello():
#    ClientId2Key = {}
#    ClientKey2Id = {}
#    ClientKey2Ws = {}
#    return {"text": "hello world!"}

#users=Users()

# 入室のエンドポイント
@app.websocket("/ws")
async def websocket_status(ws: WebSocket):
    await ws.accept()
    #print("join")
    # クライアントを識別するためのIDを取得
    key = ws.headers.get('sec-websocket-key')
    #print(ws)
    try:
        while True:
            # クライアントからメッセージを受信
            data = await ws.receive_text()
            #print()
            #print(data)
            #print()
            #入室処理
            if(json.loads(data)["type"]=="enter"):
                #print("enter")
                print("0:",rooms)
                #キーをセット
                #users.set(json.loads(data)["id"],key,ws)
                #ClientKey2Ws[key] = ws
                #ClientId2Key[json.loads(data)["id"]] = key
                #ClientKey2Id[key] = str(json.loads(data)["id"])
                
                try:
                    room=rooms[str(json.loads(data)["roomid"])]
                except:
                    print("first room user")
                    room ={}
                room.update({str(json.loads(data)["id"]):ws})
                rooms.update({str(json.loads(data)["roomid"]):room})
                print("1:",rooms)

                #print("[keys]")
                #print(ClientId2Key)
                #print(ClientKey2Id)
                #print(ClientKey2Ws)                
                members = r.hgetall("room:"+str(json.loads(data)["roomid"]))
                for member in members.values():
                    #print("sending newuser msg:",member)
                    try:
                        print("2:",rooms)

                        client=rooms[str(json.loads(data)["roomid"])][member.decode()]
                        print("3:",rooms)
                        
                        #print("sent newuser msg:",member)
                        #print(member.decode(),client)
                        txt="{\"type\":\"users\",\"users\":"+str([l.decode() for l in members.values() ]).replace("'","\"")+"}"
                        #print("send:",txt)
                        await client.send_text(txt)
                        #await client.send_text("{\"type\":\"newuser\",\"id\":\""+json.loads(data)["id"]+"\"}")
                    except:
                        print("newuser error")
                        #print()
                        #print(ClientId2Key)
                        #print()
                        import traceback
                        traceback.print_exc()
                        #print(members,member)
                        #print(ClientId2Key)
                        #print(ClientKey2Id)
                        #print(ClientKey2)
                        


         #@author Tanaka Koki

            #グループ全送信系の操作
            elif(json.loads(data)["type"] in ["status","progress","g_message"]):
                print("group message")
                #print(json.loads(data)["type"])
                members = r.hgetall("room:"+str(json.loads(data)["roomid"]))
                for member in members.values():
                    try:
                        client=rooms[str(json.loads(data)["roomid"])][member.decode()]
                        await client.send_text(data)
                    except:
                        import traceback
                        traceback.print_exc()
                        print("groupmessage error")
                        print(rooms)
                        print()
                        #print(members,member)


        #@author Tanaka Koki
        
            #通話リクエスト
            elif(json.loads(data)["type"] in ["call_request"]):
                print("call  requested")
                print(json.loads(data)["type"])   
                try:             
                    to = json.loads(data)["to"]
                    fromid = json.loads(data)["from"]
                except:
                    print("room id error:")
                print("call request to ",to," from " ,fromid)
                print("online status:",r.keys("online:"+str(to)))
                if(("online:"+str(to)).encode() in r.keys("online:"+str(to))):# オンライン時
                    print(rooms)
                    try:
                        print("sending call msg:",fromid,to)                        
                        client=rooms[str(r.hget("user:"+to,"roomid").decode())][to]
                        callid=int(random.uniform(0, 2**16))
                        s_data="{\"type\":\"call_start\",\"value\":\""+str(callid)+"\",\"from\":\""+str(fromid)+"\",\"to\":\""+str(to)+"\"}"
                        print("sending data:",s_data)
                        await client.send_text(s_data)
                        print("sending call msg:to self")                        
                        await ws.send_text(s_data)

                    except:
                        import traceback
                        traceback.print_exc()
                        print("personal call msg error")
                        #print(ClientId2Key)
                        #print(ClientKey2Id)
                        #print(ClientKey2Ws)                      
                else:# オフライン時          
                    client=ws
                    await client.send_text("{\"type\":\"i_message_fail\",\"value\":\"failed in sending\",\"from\":\""+fromid+"\",\"to\":\""+fromid+"\"}")



        #@author Suzuki Hijiri
        #個人チャット
        #@author Tanaka Koki
        #招待
        
            elif(json.loads(data)["type"] in ["i_message","invite","call_deny","call_end"]):
                print("personal  message")
                #print(json.loads(data)["type"])                

                to = json.loads(data)["to"]
                fromid = json.loads(data)["from"]
                print("message to ",to," from " ,fromid)
                #print("online status:",r.keys("online:"+to))
                if(("online:"+to).encode() in r.keys("online:"+to)):# オンライン時
                    #print(ClientId2Key)
                    #print(ClientKey2Ws)
                    try:
                        print("sending personal msg:",fromid,to)                        
                        client=rooms[str(r.hget("user:"+to,"roomid").decode())][to]
                        await client.send_text(data)
                    except:
                        import traceback
                        traceback.print_exc()

                        print("personalmsg error")
                        #print(members,member)
                        #print(ClientId2Key)
                        #print(ClientKey2Id)
                        #print(ClientKey2Ws)                      
                else:# オフライン時          
                    client=ws
                    await client.send_text("{\"type\":\"i_message_fail\",\"value\":\"failed in sending\",\"from\":\""+fromid+"\",\"to\":\""+fromid+"\"}")

        #@author Tanaka Koki
        
    except WebSocketDisconnect:
        print("disconnection message")
        userid=""
        for dd in rooms.values():
            userid=[k for k,v in dd.items() if v==ws][0]
        print("disconnected："+userid)
        try:
            print(rooms[r.hget("user:"+userid,"roomid").decode()])
            rooms[r.hget("user:"+userid,"roomid").decode()].pop(userid)
        except:
            print("pop error")
            import traceback
            traceback.print_exc()

        print(rooms)
        r.delete("online:"+userid)
        r.hset("user:"+userid,"online",'false')

        # idからroom取得
        roomid=r.hget("user:"+str(userid),"roomid")
        room_userid=[k for k, v in r.hgetall("room:"+str(roomid.decode())).items() if v == userid .encode()]
        print("left room:",r.hgetall("room:"+str(roomid.decode())).items())
        try:
            r.hdel("room:"+roomid.decode(),room_userid[0].decode())
        except:
            print("delete error")
        print("→left room:",r.hgetall("room:"+str(roomid.decode())).items())
        print("leaving person:","roomid:",roomid," room key:",room_userid)
        sum_login_time=0
        try:
            sum_login_time=int(r.hget("user:"+str(userid),"sum_login_time").decode())
            #タイムスタンプの取得とログイン時間の加算
            sum_login_time+=int(time.time())-int(r.hget("user:"+str(userid),"login_time").decode())
            r.hset("user:"+userid,"sum_login_time",str(sum_login_time))
        except:
            print("logintime update error")
            import traceback
            traceback.print_exc()
            
            #@author Suzuki Hijiri
            
        #総ログイン時間ごとのランク更新
        day=24*60*60
        try:
            rank=r.hget("user:"+str(userid),"rank").decode()
            print(rank)
        except:
            print("rank get error")
            rank="砂"
        if(rank!="カリホルニウム"):
            if(sum_login_time<1*day):
                if(rank!="砂"):
                    r.hset("user:"+userid,"rank","砂")
            elif(sum_login_time<2*day):
                if(rank!="砂利"):
                    r.hset("user:"+userid,"rank","砂利")
            elif(sum_login_time<5*day):
                if(rank!="石"):
                    r.hset("user:"+userid,"rank","石")
            elif(sum_login_time<10*day):
                if(rank!="くず鉄"):
                    r.hset("user:"+userid,"rank","くず鉄")
            elif(sum_login_time<20*day):
                if(rank!="鉄"):
                    r.hset("user:"+userid,"rank","鉄")
            elif(sum_login_time<30*day):
                if(rank!="ブロンズ"):
                    r.hset("user:"+userid,"rank","ブロンズ")
            elif(sum_login_time<50*day):
                if(rank!="シルバー"):
                    r.hset("user:"+userid,"rank","シルバー")
            elif(sum_login_time<80*day):
                if(rank!="ゴールド"):
                    r.hset("user:"+userid,"rank","ゴールド")
            elif(sum_login_time<130*day):
                if(rank!="プラチナ"):
                    r.hset("user:"+userid,"rank","プラチナ")
            elif(sum_login_time<190*day):
                if(rank!="ダイヤモンド"):
                    r.hset("user:"+userid,"rank","ダイヤモンド")
            elif(sum_login_time<260*day):
                if(rank!="ロジウム"):
                    r.hset("user:"+userid,"rank","ロジウム")
            elif(sum_login_time<365*day):
                if(rank!="オスミウム"):
                    r.hset("user:"+userid,"rank","オスミウム")
            
        print("rank renewed")
        #実質broadcast others
        members = r.hgetall("room:"+roomid.decode())
        for member in members.values():
            try:
                print("sending leaving msg:",member)
                client=rooms[r.hget("user:"+member.decode(),"roomid").decode()][member.decode()]
                await client.send_text("{\"type\":\"leave\",\"id\":\""+userid+"\"}")
            except:
                print("failed in sending leave message")
                import traceback
                traceback.print_exc()

        #ルームから抜ける
            

    


if __name__ == '__main__':
    uvicorn.run(host="0.0.0.0",app=app)#,port=8000)


