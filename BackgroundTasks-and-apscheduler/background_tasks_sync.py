from fastapi import FastAPI, BackgroundTasks
import time
from datetime import datetime

app = FastAPI()

def write_log(message: str):
  # 獲取當前時間
  time.sleep(5)   # 模擬任務耗時
  current_time = datetime.now().strftime("%H:%M:%S")
  with open("log.txt", "a") as log_file:
    log_file.write(f"[{current_time}] {message}\n")
    
@app.get("/")
async def root(background_tasks: BackgroundTasks):
  # 獲取當前時間
  current_time = datetime.now().strftime("%H:%M:%S")
  # 背景執行任務，這裡將寫入日誌的操作放入背景
  background_tasks.add_task(write_log, f"New request received at {current_time}")
  return {"message": "Request received, task in background", "time": current_time}