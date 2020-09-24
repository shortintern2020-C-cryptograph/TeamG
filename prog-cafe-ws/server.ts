import http from 'http';
import WebSocket from 'ws';
import express from 'express';
import Redis from 'ioredis';
const r = new Redis('redis://h:p67a72fdc9e0b5ff64d97388a2890aad0f232e1345a94014540b23bcdd14f4242@ec2-50-16-12-122.compute-1.amazonaws.com:15169');
const app = express();
app.use(express.static('public'));
const port = process.env.PORT || 9090;
const server = http.createServer(app);

type Room = {
  [userId: string]: WebSocket | undefined;
}

const wss = new WebSocket.Server({ server });
const rooms: Record<string, Room> = {};

const broadcast = (socks: Room | null, content: Record<string, unknown>, self = '') => {
  if (!socks) return;
  Object.keys(socks).forEach((userId) => {
    if (self === userId) return;
    socks[userId]?.send(JSON.stringify(content));
  });
};

const send = (sock: WebSocket | undefined, content: Record<string, unknown>) => {
  if (!sock) return;
  sock.send(JSON.stringify(content));
};

const randomString = () => Math.random().toString(32).substring(2);

wss.on('connection', (ws) => {
  let userId: string | null = null;
  let roomId: string | null = null;

  ws.on('open', () => {
    console.log('new ws');
  });

  ws.on('close', () => {
    console.log('close', { userId, roomId });
    if (userId == null || roomId == null) {
      console.log('cannot get ids', { userId, roomId });
      return;
    }
    delete rooms[roomId][userId];
    broadcast(rooms[roomId], {
      type: 'leave',
      id: userId,
    }, userId);

    r.hgetall(`room:${roomId}`).then((res) => {
      Object.entries(res).forEach(([key, value]) => {
        console.log({ key, value });
        if (value === userId) r.hdel(`room:${roomId}`, key);
      });
    }).then(console.log).catch(console.error);
    r.del(`online:${userId}`).then(console.log).catch(console.error);
    r.hset(`user:${userId}`, 'online', 'false').then(console.log).catch(console.error);
  });

  ws.on('message', (data) => {
    const json = JSON.parse(data.toString()) as Record<string, string>;
    console.log('incoming message', json.type, json);
    switch (json.type) {
      case 'enter':
        userId = json.id;
        roomId = json.roomid;
        if (userId == null || roomId == null) {
          console.log('cannot get ids', { userId, roomId });
          break;
        }
        console.log('enter', { userId, roomId });
        if (!rooms[roomId]) rooms[roomId] = {};
        rooms[roomId][userId] = ws;
        broadcast(rooms[roomId], {
          type: 'users',
          users: Object.keys(rooms[roomId]),
        });
        break;
      case 'status':
      case 'progress':
      case 'g_message':
        if (roomId == null) {
          console.log('cannot get ids', { userId, roomId });
          break;
        }
        broadcast(rooms[roomId], json);
        break;
      case 'i_message':
        if (roomId == null) {
          console.log('cannot get ids', { userId, roomId });
          break;
        }
        send(rooms[roomId][json.to], json);
        break;
      case 'call_request': {
        if (roomId == null) {
          console.log('cannot get ids', { userId, roomId });
          break;
        }
        const sendData = {
          ...json,
          type: 'call_start',
          value: randomString(),
        };
        send(rooms[roomId][json.from], sendData);
        send(rooms[roomId][json.to], sendData);
      }
        break;
      case 'call_deny':
        if (roomId == null) {
          console.log('cannot get ids', { userId, roomId });
          break;
        }
        send(rooms[roomId][json.to], {
          ...json,
          type: 'call_deny',
        });
        break;
      case 'call_end': {
        if (roomId == null) {
          console.log('cannot get ids', { userId, roomId });
          break;
        }
        const sendData = {
          ...json,
          type: 'call_end',
        };
        send(rooms[roomId][json.from], sendData);
        send(rooms[roomId][json.to], sendData);
      }
        break;
      case 'invite': {
        const roomid = Object.keys(rooms).find((id) => Object.keys(rooms[id]).includes(json.to));
        if (roomid == null) {
          console.log('cannot get ids', { userId, roomId });
          break;
        }
        send(rooms[roomid][json.to], json);
      }
        break;
      default:
        console.log('undefined type');
    }
  });
});

server.listen(port);
