from fastapi import FastAPI, BackgroundTasks
import asyncio
from datetime import datetime

app = FastAPI()

async def send_email(email: str):
  # 模擬發送電子郵件的非同步任務
  await asyncio.sleep(5)
  current_time = datetime.now().strftime("%H:%M:%S")
  print(f"Email sent to {email}, {current_time}")
  
@app.get("/send_email/")
async def send_background_email(email: str, background_tasks: BackgroundTasks):
  # 將發送電子郵件的任務加入背景
  background_tasks.add_task(send_email, email)
  return {"message": f"Email will be sent to {email}"}