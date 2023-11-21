from datetime import datetime
from enum import Enum

import socketio


class EventName(Enum):
    send = 'send'
    receive = 'receive'
    room_joined = 'room_joined'
    room_message = 'room_message'


sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[
        'http://localhost:8000',
        'https://admin.socket.io',  # edit the allowed origins if necessary
    ])


@sio.event
async def connect(sid: str, environ):
    await sio.emit('status', {'data': 'Connected', 'count': 0})


@sio.event
async def send(sid, message):
    print(message)
    current_time = datetime.now()
    time_format = '%Y-%m-%d %H:%M:%S'

    time_string = current_time.strftime(time_format)
    print(time_string)

    response = {'data': message['message'], 'message': f'message received', 'timestamp': time_string}
    await sio.emit(EventName.receive.name, response)


@sio.event
async def join_room(sid: str, message: dict):
    room = message['room']
    response = f'Entered room: {room} with sid {sid}'
    print(response)
    await sio.enter_room(sid, room)
    await sio.emit(EventName.room_joined.name, {'data': response},
                   room=room, skip_sid=sid)


@sio.event
async def send_webrtc_offer(sid: str, message: dict):
    room = message['room']
    print(f'send_webrtc_offer received in room {room}')
    await sio.emit('offer', message,
                   room=room, skip_sid=sid)


@sio.event
async def room_message(sid: str, message: dict):
    room = message['room']
    print(f'New message in room {room} from SID: {sid}')

    await sio.emit(EventName.room_message.name, message,
                   room=room, skip_sid=sid)


@sio.event
async def leave_room(sid: str, message: dict):
    await sio.leave_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Left room: ' + message['room']},
                   room=sid)


@sio.event
async def close_room(sid: str, message: dict):
    await sio.emit('my_response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])


@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)
