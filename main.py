import uvicorn
from fastapi import FastAPI

from api import api
from socket_io import socket_io_service

app = FastAPI()

app.include_router(api.router)

app.mount("/", socket_io_service.socketio.ASGIApp(socket_io_service.sio))

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
