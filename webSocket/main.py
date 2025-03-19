from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from typing import List

app = FastAPI()

# 管理多個客戶端的連接
class ConnectionManger:
  def __init__(self):
    self.active_connections: List[WebSocket] = []

  async def connect(self, websocket: WebSocket):
    await websocket.accept()
    self.active_connections.append(websocket)
  
  def disconnect(self, websocket: WebSocket):
    self.active_connections.remove(websocket)
  
  async def send_message(self, message: str, websocket: WebSocket):
    await websocket.send_text(message)
  
  async def broadcast(self, message: str):
    for connection in self.active_connections:
      await connection.send_text(message)

# 建立連接管理器
manger = ConnectionManger()

@app.get("/")
async def get():
  return FileResponse("index.html")

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
  await manger.connect(websocket)
  try:
    while True:
      data = await websocket.receive_text()
      await manger.broadcast(f"Client says: {data}")
  except WebSocketDisconnect:
    manger.disconnect(websocket)
    await manger.broadcast("A clent disconnected")