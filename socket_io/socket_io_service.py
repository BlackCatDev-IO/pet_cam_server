from datetime import datetime
from enum import Enum

import socketio


class EventName(Enum):
    send = 'send'
    receive = 'receive'


sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[
        'http://localhost:8000',
        'https://admin.socket.io',  # edit the allowed origins if necessary
    ])


@sio.event
async def connect(sid, environ):
    await sio.emit('status', {'data': 'Connected', 'count': 0}, room=sid)


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
async def join_room(sid, message):
    room = message['room']
    response = f'Entered room: {room} with sid {sid}'
    print(response)
    await sio.enter_room(sid, room)
    await sio.emit('my_response', {'data': response},
                   room=sid)


@sio.event
async def leave_room(sid, message):
    await sio.leave_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Left room: ' + message['room']},
                   room=sid)


@sio.event
async def close_room(sid, message):
    await sio.emit('my_response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])


@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)
